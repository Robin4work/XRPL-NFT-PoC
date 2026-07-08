from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.nft_v2 import router as nft_v2_router
from app.routes.nft import router as nft_router

app = FastAPI(title="Gemstone NFT API")
app.include_router(nft_v2_router)

# Allow the Next.js frontend to call this API.
# FRONTEND_ORIGIN is set in Railway's env vars to your Vercel URL in production;
# localhost:3000 stays allowed for local dev.
import os

allowed_origins = ["http://localhost:3000"]
frontend_origin = os.getenv("FRONTEND_ORIGIN")
if frontend_origin:
    allowed_origins.append(frontend_origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(nft_router)

@app.get("/")
def root():
    return {"message": "Gemstone NFT API Running 🚀"}