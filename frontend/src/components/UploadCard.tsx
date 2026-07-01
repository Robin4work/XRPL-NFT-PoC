"use client";

import { useRef, useState } from "react";

interface UploadCardProps {
  onMint: (file: File) => void;
  isMinting: boolean;
}

export default function UploadCard({ onMint, isMinting }: UploadCardProps) {
  const [file, setFile] = useState<File | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0] ?? null;
    setFile(selected);
  };

  return (
    <div className="card">
      <h2>1. Upload Raman CSV</h2>

      <label className="file-drop" htmlFor="csv-input">
        <input
          id="csv-input"
          ref={inputRef}
          type="file"
          accept=".csv"
          onChange={handleFileChange}
        />
        {file ? (
          <span className="filename">{file.name}</span>
        ) : (
          "Click to choose a .csv file"
        )}
      </label>

      <button
        className={`primary${isMinting ? " loading" : ""}`}
        disabled={!file || isMinting}
        onClick={() => file && onMint(file)}
      >
        {isMinting
          ? "Fingerprinting & Minting…"
          : "Generate Fingerprint & Mint NFT"}
      </button>

      <p className="hint">
        The CSV is hashed with SHA3-256 on the backend. The hash is stored as
        the NFT&apos;s URI when it&apos;s minted on XRPL Testnet — it&apos;s
        never uploaded anywhere else.
      </p>
    </div>
  );
}
