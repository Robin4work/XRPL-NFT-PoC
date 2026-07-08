from app.services.xrpl_service import mint_nft


async def mint_from_metadata(metadata: dict, fingerprint: str):
    # NFT URI field is capped at 512 hex chars (256 bytes) on XRPL, so we can't
    # fit full metadata on-chain. We store only the short SHA3-256 fingerprint
    # as the on-chain pointer; the full metadata is already saved off-chain
    # via save_metadata() in the mint route.
    result = await mint_nft(fingerprint)

    return {
        "uri": fingerprint,
        "nft_id": result["nft_id"],
        "tx_hash": result["tx_hash"],
    }