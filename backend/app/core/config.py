from dotenv import load_dotenv
import os

load_dotenv()


class Settings:

    XRPL_RPC = os.getenv("XRPL_RPC")

    SELLER_SEED = os.getenv("SELLER_SEED")
    BUYER_SEED = os.getenv("BUYER_SEED")


settings = Settings()