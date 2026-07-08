# from pydantic import BaseModel
# from typing import Optional


# class NFTMetadata(BaseModel):
#     puf_hash: str

#     stone_id: Optional[str] = None
#     certificate_number: Optional[str] = None

#     laboratory: Optional[str] = None
#     species: Optional[str] = None

#     carat_weight: Optional[float] = None
#     color: Optional[str] = None
#     clarity: Optional[str] = None

#     treatment: Optional[str] = None
#     origin: Optional[str] = None
#     natural_origin: Optional[str] = None

#     raman_laser_nm: Optional[int] = None
#     raman_snr: Optional[float] = None

#     scan_date: Optional[str] = None
#     emission_date: Optional[str] = None

#     wallet_vendeur: Optional[str] = None

#     network: str = "XRPL Testnet"

from pydantic import BaseModel
from typing import Optional


class NFTMetadata(BaseModel):
    puf_hash: str

    stone_id: Optional[str] = None
    certificate_number: Optional[str] = None

    laboratory: Optional[str] = None
    species: Optional[str] = None

    carat_weight: Optional[float] = None
    color: Optional[str] = None
    clarity: Optional[str] = None

    treatment: Optional[str] = None
    origin: Optional[str] = None
    natural_origin: Optional[str] = None

    raman_laser_nm: Optional[int] = None
    raman_snr: Optional[float] = None

    scan_date: Optional[str] = None
    emission_date: Optional[str] = None

    wallet_vendeur: Optional[str] = None

    network: str = "XRPL Testnet"

    documents: Optional[dict] = None