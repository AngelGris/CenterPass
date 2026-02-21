from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.ingestion.extract_frames import extract_frames
from app.services.video_service import save_video
from database.session import get_db

router = APIRouter(prefix="/videos", tags=["videos"])

ALLOWED_VIDEO_TYPES = {
    "video/mp4",
    "video/quicktime",
    "video/x-matroska",
}


@router.post("/upload")
async def upload_video(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = None,
):
    if file.content_type not in ALLOWED_VIDEO_TYPES:
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only MP4, MOV and MKV are allowed."
        )

    result = await save_video(file=file, db=db)

    # Run frame extraction in background
    background_tasks.add_task(extract_frames, result["video_id"])

    return {
        "video_id": str(result["video_id"]),
        "message": "Upload successful. Frame extraction started.",
    }
