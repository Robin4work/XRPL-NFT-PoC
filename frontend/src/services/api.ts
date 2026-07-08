const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export interface MintResponse {
  status: string;
  job_id: string;
  fingerprint: string;
  nft_id: string;
  tx_hash: string;
  explorer: string;
  metadata: Record<string, unknown>;
}

export interface TransferResponse {
  status: string;
  tx_hash: string;
}

export interface MintFiles {
  ramanFile: File;
  ftirFile?: File | null;
  uvFile?: File | null;
  images?: File[];
  certificate?: CertificateDetails;
}

export interface CertificateDetails {
  stoneId?: string;
  certificateNumber?: string;
  laboratory?: string;
  species?: string;
  caratWeight?: string;
  color?: string;
  clarity?: string;
  treatment?: string;
  origin?: string;
  naturalOrigin?: string;
  emissionDate?: string;
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
 * Uploads the lab file bundle (Raman required; FTIR/UV/images optional),
 * plus manually-entered certificate details, to the /nft-v2/mint endpoint.
 * The backend hashes the Raman spectrum (SHA3-256) and mints an NFT on
 * XRPL Testnet with that hash as the URI, while the full certificate
 * metadata is saved off-chain.
 */
export async function mintNft(files: MintFiles): Promise<MintResponse> {
  const formData = new FormData();
  formData.append("raman_file", files.ramanFile);

  if (files.ftirFile) {
    formData.append("ftir_file", files.ftirFile);
  }
  if (files.uvFile) {
    formData.append("uv_file", files.uvFile);
  }
  if (files.images) {
    for (const image of files.images) {
      formData.append("images", image);
    }
  }

  const c = files.certificate;
  if (c) {
    if (c.stoneId) formData.append("stone_id", c.stoneId);
    if (c.certificateNumber) formData.append("certificate_number", c.certificateNumber);
    if (c.laboratory) formData.append("laboratory", c.laboratory);
    if (c.species) formData.append("species", c.species);
    if (c.caratWeight) formData.append("carat_weight", c.caratWeight);
    if (c.color) formData.append("color", c.color);
    if (c.clarity) formData.append("clarity", c.clarity);
    if (c.treatment) formData.append("treatment", c.treatment);
    if (c.origin) formData.append("origin", c.origin);
    if (c.naturalOrigin) formData.append("natural_origin", c.naturalOrigin);
    if (c.emissionDate) formData.append("emission_date", c.emissionDate);
  }

  const res = await fetch(`${API_BASE_URL}/nft-v2/mint`, {
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