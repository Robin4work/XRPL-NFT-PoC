// Thin wrapper around the FastAPI backend.
// Two endpoints, two functions -- no client, no generics, no over-engineering.

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export interface MintResponse {
  status: string;
  fingerprint: string;
  nft_id: string;
  tx_hash: string;
  explorer: string;
}

export interface TransferResponse {
  status: string;
  tx_hash: string;
}

async function parseErrorMessage(res: Response): Promise<string> {
  try {
    const body = await res.json();
    return body.detail || res.statusText;
  } catch {
    return res.statusText;
  }
}

/**
 * Uploads a Raman CSV to the backend, which hashes it (SHA3-256) and
 * mints an NFT on XRPL Testnet containing that hash as the NFT URI.
 */
export async function mintNft(file: File): Promise<MintResponse> {
  const formData = new FormData();
  formData.append("csv_file", file);

  const res = await fetch(`${API_BASE_URL}/nft/mint`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    throw new Error(await parseErrorMessage(res));
  }

  return res.json();
}

/**
 * Transfers a previously minted NFT from Wallet A (seller) to Wallet B
 * (buyer) via the backend's create-offer / accept-offer flow.
 */
export async function transferNft(nftId: string): Promise<TransferResponse> {
  const res = await fetch(
    `${API_BASE_URL}/nft/transfer/${encodeURIComponent(nftId)}`,
    { method: "POST" }
  );

  if (!res.ok) {
    throw new Error(await parseErrorMessage(res));
  }

  return res.json();
}
