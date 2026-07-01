import hashlib
import pandas as pd

CSV_PATH = "data/spectral.csv"

# Read CSV
df = pd.read_csv(CSV_PATH)

# Normalize the data
df = df.round(6)

# Convert to deterministic string
csv_string = df.to_csv(index=False, lineterminator="\n")

# Generate SHA3-256 hash
fingerprint = hashlib.sha3_256(csv_string.encode("utf-8")).hexdigest()

print("\nCSV Loaded Successfully ✅")
print(f"Rows: {len(df)}")
print(f"\nSHA3-256 Fingerprint:\n{fingerprint}")