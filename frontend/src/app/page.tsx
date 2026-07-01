"use client";

import { useState } from "react";
import UploadCard from "@/components/UploadCard";
import ResultPanel from "@/components/ResultPanel";
import {
  mintNft,
  transferNft,
  MintResponse,
  TransferResponse,
} from "@/services/api";

export default function Home() {
  const [mintResult, setMintResult] = useState<MintResponse | null>(null);
  const [transferResult, setTransferResult] = useState<TransferResponse | null>(
    null
  );
  const [isMinting, setIsMinting] = useState(false);
  const [isTransferring, setIsTransferring] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleMint = async (file: File) => {
    setError(null);
    setTransferResult(null);
    setIsMinting(true);
    try {
      const result = await mintNft(file);
      setMintResult(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Minting failed.");
    } finally {
      setIsMinting(false);
    }
  };

  const handleTransfer = async () => {
    if (!mintResult) return;
    setError(null);
    setIsTransferring(true);
    try {
      const result = await transferNft(mintResult.nft_id);
      setTransferResult(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Transfer failed.");
    } finally {
      setIsTransferring(false);
    }
  };

  return (
    <main>
      <header className="page-header">
        <h1>Raman Spectrum → NFT</h1>
        <p>
          Upload a Raman CSV to fingerprint it (SHA3-256), mint it as an NFT
          on XRPL Testnet, then transfer it between two test wallets.
        </p>
      </header>

      {error && <div className="error-banner">{error}</div>}

      <UploadCard onMint={handleMint} isMinting={isMinting} />

      {mintResult && (
        <ResultPanel
          mintResult={mintResult}
          transferResult={transferResult}
          onTransfer={handleTransfer}
          isTransferring={isTransferring}
        />
      )}
    </main>
  );
}
