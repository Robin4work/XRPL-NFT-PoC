import os
import uuid
import shutil
from fastapi import UploadFile


TEMP_FOLDER = "temp"

os.makedirs(TEMP_FOLDER, exist_ok=True)


def save_upload_file(file: UploadFile):

    extension = os.path.splitext(file.filename)[1]

    filename = f"{uuid.uuid4()}{extension}"

    path = os.path.join(TEMP_FOLDER, filename)

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return path


def delete_file(path):

    if os.path.exists(path):
        os.remove(path)