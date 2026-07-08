"use client";

import { useState } from "react";
import { MintFiles } from "@/services/api";

interface UploadCardProps {
  onMint: (files: MintFiles) => void;
  isMinting: boolean;
}

function FileSlot({
  id,
  label,
  file,
  onChange,
  placeholder,
  multiple = false,
}: {
  id: string;
  label: string;
  file: File | File[] | null;
  onChange: (fileList: FileList | null) => void;
  placeholder: string;
  multiple?: boolean;
}) {
  const displayName = Array.isArray(file)
    ? file.map((f) => f.name).join(", ")
    : file?.name;

  return (
    <div style={{ marginBottom: "10px" }}>
      <label
        className="file-drop"
        htmlFor={id}
        style={{ display: "block", padding: "12px" }}
      >
        <input
          id={id}
          type="file"
          multiple={multiple}
          onChange={(e) => onChange(e.target.files)}
        />
        <div
          style={{
            fontSize: "11px",
            color: "var(--muted)",
            marginBottom: "3px",
          }}
        >
          {label}
        </div>
        {displayName ? (
          <span className="filename">{displayName}</span>
        ) : (
          placeholder
        )}
      </label>
    </div>
  );
}

export default function UploadCard({ onMint, isMinting }: UploadCardProps) {
  const [ramanFile, setRamanFile] = useState<File | null>(null);
  const [ftirFile, setFtirFile] = useState<File | null>(null);
  const [uvFile, setUvFile] = useState<File | null>(null);
  const [images, setImages] = useState<File[]>([]);

  const handleSubmit = () => {
    if (!ramanFile) return;
    onMint({
      ramanFile,
      ftirFile,
      uvFile,
      images,
    });
  };

  return (
    <div className="card">
      <h2>1. Upload Lab Files</h2>

      <FileSlot
        id="raman-input"
        label="Raman spectrum (required) — extracted .txt, not the .zip"
        file={ramanFile}
        onChange={(files) => setRamanFile(files?.[0] ?? null)}
        placeholder="Click to choose the Raman .txt file"
      />

      <FileSlot
        id="ftir-input"
        label="FTIR spectrum (optional) — extracted .CSV, not the .zip"
        file={ftirFile}
        onChange={(files) => setFtirFile(files?.[0] ?? null)}
        placeholder="Click to choose the FTIR .CSV file"
      />

      <FileSlot
        id="uv-input"
        label="UV-Vis spectrum (optional)"
        file={uvFile}
        onChange={(files) => setUvFile(files?.[0] ?? null)}
        placeholder="Click to choose the UV .txt file"
      />

      <FileSlot
        id="images-input"
        label="Stone photos (optional, multiple allowed)"
        file={images}
        onChange={(files) => setImages(files ? Array.from(files) : [])}
        placeholder="Click to choose one or more photos"
        multiple
      />

      <button
        className={`primary${isMinting ? " loading" : ""}`}
        disabled={!ramanFile || isMinting}
        onClick={handleSubmit}
      >
        {isMinting
          ? "Fingerprinting & Minting…"
          : "Generate Fingerprint & Mint NFT"}
      </button>

      <p className="hint">
        Only the Raman spectrum is hashed (SHA3-256) and stored as the
        NFT&apos;s on-chain URI. The full certificate — including FTIR/UV data
        and photos — is saved off-chain; XRPL&apos;s URI field can&apos;t hold
        more than 512 characters.
      </p>
    </div>
  );
}
