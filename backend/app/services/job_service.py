import json
import os


def save_metadata(job_path: str, metadata: dict):

    file_path = os.path.join(
        job_path,
        "metadata.json"
    )

    with open(file_path, "w", encoding="utf-8") as f:

        json.dump(
            metadata,
            f,
            indent=4,
            ensure_ascii=False,
        )

    return file_path