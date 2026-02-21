import logging
import os
import time
from datetime import datetime, timezone
from uuid import UUID

import cv2
from sqlalchemy.orm import Session

from app.core.settings import settings
from database.database import SessionLocal
from database.enums.video_processing_status import VideoProcessingStatus
from database.models import Frame, Video

logger = logging.getLogger(__name__)

FRAMES_DIR = settings.FRAME_STORAGE_PATH
TARGET_FPS = 5  # Extract 5 frame per second


def extract_frames(video_id: UUID) -> None:
    """
    Background task:
    - Loads video from DB
    - Extracts frames
    - Saves frames to disk
    - Inserts Frame records
    - Updates video metadata
    """

    db: Session = SessionLocal()

    try:
        video = db.query(Video).filter(Video.id == video_id).first()
        if not video:
            return

        cap = cv2.VideoCapture(video.filepath)

        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps else 0

        progress_interval = max(1, total_frames // 20)

        video_frames_dir = os.path.join(FRAMES_DIR, str(video.id))
        os.makedirs(video_frames_dir, exist_ok=True)

        frames_to_extract = total_frames // (fps / TARGET_FPS) if fps else total_frames
        frame_number = 0
        saved_frame_count = 0
        next_capture_time = 0
        start_time = time.time()

        # Update metadata
        video.fps = fps
        video.duration = duration
        video.processing_status = VideoProcessingStatus.PROCESSING
        db.commit()

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            current_time = frame_number / fps
            if current_time >= next_capture_time:
                timestamp = frame_number / fps if fps else 0

                frame_filename = f"frame_{frame_number:06d}.jpg"
                frame_path = os.path.join(video_frames_dir, frame_filename)

                cv2.imwrite(frame_path, frame)

                frame_record = Frame(
                    video_id=video.id,
                    frame_number=frame_number,
                    timestamp=timestamp,
                    filepath=frame_path,
                )

                db.add(frame_record)
                saved_frame_count += 1
                next_capture_time += 1 / TARGET_FPS

            frame_number += 1

            if frame_number % progress_interval == 0:
                progress = (frame_number / total_frames) * 100
                elpased_time = time.time() - start_time
                fps_processing = frame_number / elpased_time if elpased_time > 0 else 0
                time_left = (
                    (total_frames - frame_number) / fps_processing if fps_processing > 0 else 0
                )

                video.processing_progress = progress
                db.commit()

                logger.info(
                    f"Video {video.id}: "
                    f"Extracted {saved_frame_count}/{frames_to_extract} frames ({progress:.1f}%) "
                    f"at {fps_processing:.2f}fps. Time left: {time_left:.2f}s"
                )

        video.processing_progress = 100.0
        video.processing_status = VideoProcessingStatus.COMPLETED
        video.processed_at = datetime.now(timezone.utc).isoformat()
        db.commit()
        cap.release()

        print(f"Extracted {saved_frame_count} frames for video {video.id}")

    finally:
        db.close()
