import os
import shutil
from uuid import uuid4

from fastapi import UploadFile

from app.core.settings import settings

UPLOAD_DIR = settings.VIDEO_STORAGE_PATH

os.makedirs(UPLOAD_DIR, exist_ok=True)


async def save_video(file: UploadFile):
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": unique_filename,
        "original_filename": file.filename,
        "content_type": file.content_type,
        "location": file_path,
    }
