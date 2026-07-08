import os
import uuid
import shutil
from fastapi import UploadFile

TEMP_ROOT = "jobs"


def create_job_folder():

    job_id = str(uuid.uuid4())

    job_path = os.path.join(TEMP_ROOT, job_id)

    os.makedirs(job_path, exist_ok=True)

    os.makedirs(os.path.join(job_path, "images"), exist_ok=True)

    return job_id, job_path


def save_file(file: UploadFile, folder: str, filename: str):

    path = os.path.join(folder, filename)

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return path


def cleanup(job_path):

    shutil.rmtree(job_path, ignore_errors=True)