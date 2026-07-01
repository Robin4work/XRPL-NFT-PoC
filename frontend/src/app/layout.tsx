import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Raman NFT Fingerprint",
  description: "Upload a Raman CSV, fingerprint it, mint & transfer as an NFT on XRPL Testnet",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
