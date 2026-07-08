import json
import os


def save_mint(job_path: str, data: dict):

    path = os.path.join(
        job_path,
        "mint.json",
    )

    with open(path, "w", encoding="utf-8") as f:

        json.dump(
            data,
            f,
            indent=4,
        )

    return path