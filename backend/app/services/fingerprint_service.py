import os


def save_fingerprint(job_path: str, fingerprint: str):

    file_path = os.path.join(
        job_path,
        "fingerprint.txt"
    )

    with open(file_path, "w") as f:
        f.write(fingerprint)

    return file_path