import os
from dotenv import load_dotenv

from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet

from xrpl.models.transactions import (
    NFTokenCreateOffer,
    NFTokenAcceptOffer,
)

from xrpl.transaction import submit_and_wait

load_dotenv()

client = JsonRpcClient(os.getenv("XRPL_RPC"))

seller = Wallet.from_seed(os.getenv("SELLER_SEED"))
buyer = Wallet.from_seed(os.getenv("BUYER_SEED"))

# 👇 Paste the NFT ID from the mint output
NFT_ID = "00080000A52ED3A42AEFA9B286875261AAFEF51455F2F72F949EDE44011CDBA9"

print("Creating Sell Offer...")

offer_tx = NFTokenCreateOffer(
    account=seller.address,
    nftoken_id=NFT_ID,
    amount="0",
    destination=buyer.address,
    flags=1,  # sell offer
)

offer_response = submit_and_wait(
    offer_tx,
    client,
    seller,
)

offer_index = offer_response.result["meta"]["offer_id"]

print("Offer Created!")
print("Offer ID:", offer_index)

print("\nBuyer Accepting Offer...")

accept_tx = NFTokenAcceptOffer(
    account=buyer.address,
    nftoken_sell_offer=offer_index,
)

accept_response = submit_and_wait(
    accept_tx,
    client,
    buyer,
)

print("\n✅ NFT Transferred Successfully!")

print("TX Hash:", accept_response.result["hash"])

print(
    "Explorer:",
    f"https://testnet.xrpl.org/transactions/{accept_response.result['hash']}",
)