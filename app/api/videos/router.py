from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.video_service import save_video

router = APIRouter(prefix="/videos", tags=["videos"])

ALLOWED_VIDEO_TYPES = {
    "video/mp4",
    "video/quicktime",
    "video/x-matroska",
}


@router.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_VIDEO_TYPES:
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only MP4, MOV and MKV are allowed."
        )

    result = await save_video(file)

    return {"message": "Video uploaded successfully", **result}
