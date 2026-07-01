import os
import shutil
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.hash_service import generate_csv_hash
from app.services.xrpl_service import mint_nft, transfer_nft
from app.schemas.nft import (MintResponse, TransferResponse)

router = APIRouter(prefix="/nft", tags=["NFT"])

TEMP_FOLDER = "temp"

os.makedirs(TEMP_FOLDER, exist_ok=True)


@router.post("/mint", response_model=MintResponse)
async def mint(csv_file: UploadFile = File(...)):

    if not csv_file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed."
        )

    temp_file = os.path.join(
        TEMP_FOLDER,
        f"{uuid.uuid4()}.csv"
    )

    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(csv_file.file, buffer)

    try:

        fingerprint = generate_csv_hash(temp_file)

        result = await mint_nft(fingerprint)

        return {
            "status": "success",
            "fingerprint": fingerprint,
            "nft_id": result["nft_id"],
            "tx_hash": result["tx_hash"],
            "explorer": f"https://testnet.xrpl.org/transactions/{result['tx_hash']}"
        }

    finally:

        if os.path.exists(temp_file):
            os.remove(temp_file)


@router.post("/transfer/{nft_id}", response_model=TransferResponse)
async def transfer(nft_id: str):

    result = await transfer_nft(nft_id)

    return {
        "status": "success",
        **result
    }