from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.nft import router as nft_router

app = FastAPI(title="Gemstone NFT API")

# Allow the Next.js dev server (different origin) to call this API.
# Restricted to localhost:3000 since this is a local PoC, not a public deployment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(nft_router)


@app.get("/")
def root():
    return {"message": "Gemstone NFT API Running 🚀"}