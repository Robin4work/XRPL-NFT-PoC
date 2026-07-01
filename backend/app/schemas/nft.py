from pydantic import BaseModel


class MintResponse(BaseModel):
    status: str
    fingerprint: str
    nft_id: str
    tx_hash: str
    explorer: str


class TransferResponse(BaseModel):
    status: str
    tx_hash: str