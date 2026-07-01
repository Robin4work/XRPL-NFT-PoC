import os

from dotenv import load_dotenv

from xrpl.asyncio.clients import AsyncJsonRpcClient
from xrpl.asyncio.transaction import submit_and_wait
from xrpl.models.transactions import (
    NFTokenAcceptOffer,
    NFTokenCreateOffer,
    NFTokenMint,
)
from xrpl.wallet import Wallet

from app.core.config import settings

client = AsyncJsonRpcClient(settings.XRPL_RPC)

seller = Wallet.from_seed(settings.SELLER_SEED)
buyer = Wallet.from_seed(settings.BUYER_SEED)


async def mint_nft(fingerprint: str):

    tx = NFTokenMint(
        account=seller.address,
        uri=fingerprint.encode().hex().upper(),
        flags=8,
        nftoken_taxon=0,
    )

    response = await submit_and_wait(
        tx,
        client,
        seller,
    )

    return {
        "nft_id": response.result["meta"]["nftoken_id"],
        "tx_hash": response.result["hash"],
    }


async def transfer_nft(nft_id: str):

    offer = NFTokenCreateOffer(
        account=seller.address,
        nftoken_id=nft_id,
        amount="0",
        destination=buyer.address,
        flags=1,
    )

    offer_response = await submit_and_wait(
        offer,
        client,
        seller,
    )

    offer_id = offer_response.result["meta"]["offer_id"]

    accept = NFTokenAcceptOffer(
        account=buyer.address,
        nftoken_sell_offer=offer_id,
    )

    accept_response = await submit_and_wait(
        accept,
        client,
        buyer,
    )

    return {
        "tx_hash": accept_response.result["hash"],
    }