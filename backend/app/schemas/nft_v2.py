from typing import Optional

from pydantic import BaseModel


class MintV2Response(BaseModel):

    status: str

    job_id: str

    fingerprint: Optional[str] = None

    nft_id: Optional[str] = None

    tx_hash: Optional[str] = None

    explorer: Optional[str] = None

    metadata: dict