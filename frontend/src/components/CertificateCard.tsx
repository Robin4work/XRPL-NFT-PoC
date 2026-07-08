"use client";

import { useState } from "react";
import { CertificateDetails } from "@/services/api";

interface CertificateCardProps {
  value: CertificateDetails;
  onChange: (value: CertificateDetails) => void;
}

const FIELDS: {
  key: keyof CertificateDetails;
  label: string;
  placeholder: string;
}[] = [
  {
    key: "stoneId",
    label: "Stone ID (GIT No.)",
    placeholder: "e.g. G2605070200001",
  },
  {
    key: "certificateNumber",
    label: "Certificate No.",
    placeholder: "e.g. G A64209",
  },
  {
    key: "laboratory",
    label: "Laboratory",
    placeholder: "e.g. GIT - Gem and Jewelry Institute of Thailand",
  },
  { key: "species", label: "Species", placeholder: "e.g. Natural Spinel" },
  { key: "caratWeight", label: "Carat weight", placeholder: "e.g. 1.14" },
  { key: "color", label: "Color", placeholder: "e.g. Red" },
  {
    key: "clarity",
    label: "Clarity",
    placeholder: "leave blank if not on certificate",
  },
  {
    key: "treatment",
    label: "Treatment",
    placeholder: "e.g. No indications of heating",
  },
  {
    key: "origin",
    label: "Origin",
    placeholder: "leave blank if not on certificate",
  },
  {
    key: "naturalOrigin",
    label: "Natural / Synthetic",
    placeholder: "e.g. Natural",
  },
  {
    key: "emissionDate",
    label: "Certificate date",
    placeholder: "e.g. June 23, 2026",
  },
];

export default function CertificateCard({
  value,
  onChange,
}: CertificateCardProps) {
  const [isOpen, setIsOpen] = useState(true);

  const handleFieldChange = (
    key: keyof CertificateDetails,
    fieldValue: string,
  ) => {
    onChange({ ...value, [key]: fieldValue });
  };

  const filledCount = FIELDS.filter((f) => value[f.key]).length;

  return (
    <div className="card">
      <h2
        style={{ cursor: "pointer", justifyContent: "space-between" }}
        onClick={() => setIsOpen(!isOpen)}
      >
        <span>2. Certificate Details</span>
        <span
          style={{
            fontSize: "11px",
            color: "var(--muted)",
            textTransform: "none",
            letterSpacing: 0,
          }}
        >
          {filledCount > 0 ? `${filledCount} filled` : ""} {isOpen ? "▲" : "▼"}
        </span>
      </h2>

      {isOpen && (
        <>
          <p className="hint" style={{ marginTop: 0, marginBottom: "12px" }}>
            From the lab&apos;s PDF certificate — type in what applies, leave
            the rest blank.
          </p>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr 1fr",
              gap: "8px 10px",
            }}
          >
            {FIELDS.map((field) => (
              <div
                key={field.key}
                style={{
                  gridColumn: field.key === "laboratory" ? "1 / -1" : undefined,
                }}
              >
                <label
                  htmlFor={field.key}
                  style={{
                    display: "block",
                    fontSize: "11px",
                    color: "var(--muted)",
                    marginBottom: "3px",
                  }}
                >
                  {field.label}
                </label>
                <input
                  id={field.key}
                  type="text"
                  value={value[field.key] || ""}
                  placeholder={field.placeholder}
                  onChange={(e) => handleFieldChange(field.key, e.target.value)}
                  style={{
                    width: "100%",
                    background: "var(--bg)",
                    border: "1px solid var(--border)",
                    borderRadius: "6px",
                    padding: "7px 9px",
                    color: "var(--text)",
                    fontSize: "13px",
                  }}
                />
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
