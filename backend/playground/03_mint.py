import os
import hashlib
import pandas as pd

from dotenv import load_dotenv

from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import NFTokenMint
from xrpl.transaction import submit_and_wait

load_dotenv()

CSV_PATH = "data/spectral.csv"

# Read CSV
df = pd.read_csv(CSV_PATH)
df = df.round(6)

# Deterministic CSV string
csv_string = df.to_csv(index=False, lineterminator="\n")

# SHA3-256 Fingerprint
fingerprint = hashlib.sha3_256(csv_string.encode()).hexdigest()

print(f"\nFingerprint:\n{fingerprint}\n")

client = JsonRpcClient(os.getenv("XRPL_RPC"))
wallet = Wallet.from_seed(os.getenv("SELLER_SEED"))

tx = NFTokenMint(
    account=wallet.address,
    uri=fingerprint.encode().hex().upper(),
    flags=8,
    nftoken_taxon=0,
)

response = submit_and_wait(tx, client, wallet)

result = response.result

print("✅ NFT Minted")
print("NFT ID :", result["meta"]["nftoken_id"])
print("Hash   :", result["hash"])
print("Fingerprint Stored :", fingerprint)