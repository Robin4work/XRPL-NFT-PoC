import json

from app.schemas.metadata import NFTMetadata


def build_metadata(
    parser_data: dict,
    wallet_vendeur: str,
):

    metadata = NFTMetadata(

        puf_hash=parser_data.get("puf_hash"),

        stone_id=parser_data.get("stone_id"),

        certificate_number=parser_data.get("certificate_number"),

        laboratory=parser_data.get("laboratory"),

        species=parser_data.get("species"),

        carat_weight=parser_data.get("carat_weight"),

        color=parser_data.get("color"),

        clarity=parser_data.get("clarity"),

        treatment=parser_data.get("treatment"),

        origin=parser_data.get("origin"),

        natural_origin=parser_data.get("natural_origin"),

        raman_laser_nm=parser_data.get("raman_laser_nm"),

        raman_snr=parser_data.get("raman_snr"),

        scan_date=parser_data.get("scan_date"),

        emission_date=parser_data.get("emission_date"),

        wallet_vendeur=wallet_vendeur,

        network="XRPL Testnet",

        documents={
            "raman_csv": parser_data.get("source_file"),
            "ftir_csv": parser_data.get("ftir"),
            "uv_csv": parser_data.get("uv"),
            "images": parser_data.get("images", [])
        }

    )

    return metadata.model_dump(exclude_none=True)


def metadata_to_uri(metadata: dict) -> str:

    json_string = json.dumps(
        metadata,
        separators=(",", ":")
    )

    return json_string.encode().hex().upper()