"use client";

import { MintResponse, TransferResponse } from "@/services/api";

interface ResultPanelProps {
  mintResult: MintResponse;
  transferResult: TransferResponse | null;
  onTransfer: () => void;
  isTransferring: boolean;
}

export default function ResultPanel({
  mintResult,
  transferResult,
  onTransfer,
  isTransferring,
}: ResultPanelProps) {
  return (
    <>
      <div className="card">
        <h2>
          3. Fingerprint & Mint Result <span className="pill">minted</span>
        </h2>

        <div className="row">
          <span className="label">SHA3-256 fingerprint</span>
          <span className="value">{mintResult.fingerprint}</span>
        </div>
        <div className="row">
          <span className="label">NFT ID</span>
          <span className="value">{mintResult.nft_id}</span>
        </div>
        <div className="row">
          <span className="label">Mint tx hash</span>
          <span className="value">{mintResult.tx_hash}</span>
        </div>
        <div className="row">
          <span className="label">Explorer</span>
          <a
            className="explorer-link"
            href={mintResult.explorer}
            target="_blank"
            rel="noopener noreferrer"
          >
            View mint transaction ↗
          </a>
        </div>
      </div>

      <div className="card">
        <h2>
          4. Transfer NFT (Wallet A → Wallet B)
          {transferResult && (
            <span className="pill transferred">transferred</span>
          )}
        </h2>

        {!transferResult ? (
          <>
            <button
              className={`secondary${isTransferring ? " loading" : ""}`}
              onClick={onTransfer}
              disabled={isTransferring}
            >
              {isTransferring ? "Transferring…" : "Transfer to Wallet B"}
            </button>
            <p className="hint">
              This creates a zero-amount NFT sell offer from Wallet A and
              accepts it from Wallet B — two XRPL transactions, both visible on
              the Testnet Explorer.
            </p>
          </>
        ) : (
          <>
            <div className="row">
              <span className="label">Transfer tx hash</span>
              <span className="value">{transferResult.tx_hash}</span>
            </div>
            <div className="row">
              <span className="label">Explorer</span>
              <a
                className="explorer-link"
                href={`https://testnet.xrpl.org/transactions/${transferResult.tx_hash}`}
                target="_blank"
                rel="noopener noreferrer"
              >
                View transfer transaction ↗
              </a>
            </div>
          </>
        )}
      </div>
    </>
  );
}
