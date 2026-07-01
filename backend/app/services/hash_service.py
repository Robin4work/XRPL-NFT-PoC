import hashlib
import pandas as pd


def generate_csv_hash(csv_path: str) -> str:
    df = pd.read_csv(csv_path)
    df = df.round(6)

    csv_string = df.to_csv(
        index=False,
        lineterminator="\n",
    )

    return hashlib.sha3_256(
        csv_string.encode()
    ).hexdigest()