import os
from dotenv import load_dotenv
from xrpl.wallet import Wallet
from xrpl.clients import JsonRpcClient
from xrpl.models.requests import AccountInfo
from xrpl.utils import drops_to_xrp

load_dotenv()

client = JsonRpcClient(os.getenv("XRPL_RPC"))

seller = Wallet.from_seed(os.getenv("SELLER_SEED"))

response = client.request(
    AccountInfo(account=seller.address)
)

balance = response.result["account_data"]["Balance"]

print(f"Address : {seller.address}")
print(f"Balance : {drops_to_xrp(balance)} XRP")