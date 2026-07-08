# import hashlib
# import pandas as pd


# def generate_csv_hash(csv_path: str) -> str:
#     df = pd.read_csv(csv_path)
#     df = df.round(6)

#     csv_string = df.to_csv(
#         index=False,
#         lineterminator="\n",
#     )

#     return hashlib.sha3_256(
#         csv_string.encode()
#     ).hexdigest()


import hashlib
import pandas as pd


def generate_csv_hash(csv_path: str) -> str:
    # Real instrument exports aren't always plain comma-separated CSVs with
    # a header row -- e.g. Raman .txt exports are tab-delimited with a
    # "#Wave  #Intensity" comment line. sep=None + engine="python" lets
    # pandas sniff the actual delimiter, and comment="#" skips instrument
    # metadata/comment lines so only the numeric spectrum is hashed.
    df = pd.read_csv(
        csv_path,
        sep=None,
        engine="python",
        comment="#",
        header=None,
    )
    df = df.round(6)

    csv_string = df.to_csv(
        index=False,
        header=False,
        lineterminator="\n",
    )

    return hashlib.sha3_256(
        csv_string.encode()
    ).hexdigest()