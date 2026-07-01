PROJECT OBJECTIVE

Build a Proof of Concept that:

1. Reads a Raman spectroscopy CSV file.
2. Generates a SHA3-256 fingerprint.
3. Uses the fingerprint to mint an NFT on the XRP Ledger Testnet.
4. Transfers the NFT from Wallet A (Seller) to Wallet B (Buyer).
5. Shows both transactions on the XRPL Testnet Explorer.
6. Provides clean source code with setup instructions.

---

DELIVERABLES

• Python code that reads a Raman CSV and generates a SHA3-256 fingerprint.

• A simple web interface allowing users to:

- Upload CSV
- Display generated hash
- Mint NFT

• XRPL Testnet wallet setup and configuration.

• NFT minting.

• NFT transfer from Wallet A to Wallet B.

• Demonstration where both transactions are visible on XRPL Testnet Explorer.

• Clean project structure.

• README with setup instructions.

---

TECH STACK

Frontend:

- Next

Backend:

- Python
- FastAPI

Blockchain:

- XRPL Testnet
- xrpl-py SDK

Other:

- pandas
- hashlib
- python-dotenv

---

PROJECT STRUCTURE

backend/
app.py
routes/
services/
hash_service.py
xrpl_service.py
wallet_service.py
metadata_service.py
utils/
requirements.txt
.env

frontend/
src/
components/
services/

docs/

README.md
