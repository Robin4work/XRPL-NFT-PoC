from typing import List, Optional

from fastapi import APIRouter, UploadFile, File, Form
from app.services.hash_service import generate_csv_hash
from app.services.job_service import save_metadata
from app.services.fingerprint_service import save_fingerprint
from app.services.mint_service_v2 import mint_from_metadata
from app.services.mint_artifact_service import save_mint
from app.schemas.nft_v2 import MintV2Response
from app.services.storage_service import (
    create_job_folder,
    save_file,
    cleanup,
)
from app.services.parser_service import (
    parse_raman,
    parse_ftir,
    parse_uv,
)
from app.services.metadata_service import build_metadata

router = APIRouter(
    prefix="/nft-v2",
    tags=["NFT V2"],
)


@router.post("/mint", response_model=MintV2Response)
async def mint_v2(
    raman_file: UploadFile = File(...),
    ftir_file: Optional[UploadFile] = File(None),
    uv_file: Optional[UploadFile] = File(None),
    images: List[UploadFile] = File(default=[]),
    # Certificate fields -- these come from the lab's PDF certificate, not
    # from any instrument file, so they're entered manually rather than
    # parsed. All optional: a mint with no certificate data is still valid,
    # it just won't have these fields populated.
    stone_id: Optional[str] = Form(None),
    certificate_number: Optional[str] = Form(None),
    laboratory: Optional[str] = Form(None),
    species: Optional[str] = Form(None),
    carat_weight: Optional[float] = Form(None),
    color: Optional[str] = Form(None),
    clarity: Optional[str] = Form(None),
    treatment: Optional[str] = Form(None),
    origin: Optional[str] = Form(None),
    natural_origin: Optional[str] = Form(None),
    emission_date: Optional[str] = Form(None),
):

    job_id, job_path = create_job_folder()

    try:
        # Save Raman CSV
        raman_path = save_file(
            raman_file,
            job_path,
            "raman.csv",
        )

        # Parse uploaded file
        parser_data = parse_raman(raman_path)

        # Generate fingerprint (ONLY ONCE)
        fingerprint = generate_csv_hash(raman_path)

        parser_data["puf_hash"] = fingerprint

        # Optional FTIR
        if ftir_file:
            ftir_path = save_file(
                ftir_file,
                job_path,
                "ftir.csv",
            )
            parser_data["ftir"] = parse_ftir(ftir_path)

        # Optional UV
        if uv_file:
            uv_path = save_file(
                uv_file,
                job_path,
                "uv.csv",
            )
            uv_data = parse_uv(uv_path)
            parser_data["uv"] = uv_data

            # The UV scan's comment header sometimes carries operator-entered
            # stone fields (species/color/scan_date). Only use them to fill
            # gaps -- never overwrite a value already set from the Raman file.
            for field in ("species", "color", "scan_date"):
                if not parser_data.get(field) and uv_data.get(field):
                    parser_data[field] = uv_data[field]

        # Optional Images
        parser_data["images"] = []

        if images:
            for image in images:
                image_path = save_file(
                    image,
                    f"{job_path}/images",
                    image.filename,
                )
                parser_data["images"].append(image_path)

        # Certificate fields from the form -- these take priority over
        # anything auto-derived, since a human-entered certificate value is
        # more authoritative than an instrument-file guess.
        certificate_fields = {
            "stone_id": stone_id,
            "certificate_number": certificate_number,
            "laboratory": laboratory,
            "species": species,
            "carat_weight": carat_weight,
            "color": color,
            "clarity": clarity,
            "treatment": treatment,
            "origin": origin,
            "natural_origin": natural_origin,
            "emission_date": emission_date,
        }
        for field, value in certificate_fields.items():
            if value not in (None, ""):
                parser_data[field] = value

        # Build Metadata
        metadata = build_metadata(
            parser_data=parser_data,
            wallet_vendeur="Wallet A",
        )

        metadata["puf_hash"] = fingerprint

        # Save artifacts
        save_metadata(
            job_path,
            metadata,
        )

        save_fingerprint(
            job_path,
            fingerprint,
        )
        mint_result = await mint_from_metadata(metadata, fingerprint)

        save_mint(
            job_path,
            mint_result,
        )

        return {
            "status": "prototype",
            "job_id": job_id,
            "fingerprint": fingerprint,
            "nft_id": mint_result["nft_id"],
            "tx_hash": mint_result["tx_hash"],
            "explorer": f"https://testnet.xrpl.org/transactions/{mint_result['tx_hash']}",
            "metadata": metadata,
        }

    finally:
        pass
        # cleanup(job_path)