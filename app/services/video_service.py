import os
import shutil
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.settings import settings
from database.models.video import Video

UPLOAD_DIR = settings.VIDEO_STORAGE_PATH

os.makedirs(UPLOAD_DIR, exist_ok=True)


async def save_video(
    file: UploadFile,
    db: Session,
):
    file_extension = file.filename.split(".")[-1]
    video_id = uuid4()
    unique_filename = f"{video_id}.{file_extension}"
    filepath = os.path.join(UPLOAD_DIR, unique_filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    video = Video(
        id=video_id,
        filename=file.filename,
        filepath=filepath,
    )

    db.add(video)
    db.commit()

    return {"video_id": video.id}
