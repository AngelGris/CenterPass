import uuid

from sqlalchemy import TIMESTAMP, Column, Enum, Float, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.database import Base
from database.enums.video_processing_status import VideoProcessingStatus


class Video(Base):
    __tablename__ = "videos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    fps = Column(Float)
    duration = Column(Float)
    processing_status = Column(Enum(VideoProcessingStatus), default=VideoProcessingStatus.PENDING)
    processing_progress = Column(Float, default=0.0)
    created_at = Column(TIMESTAMP, server_default=func.now())
    processed_at = Column(TIMESTAMP)

    frames = relationship("Frame", back_populates="video", cascade="all, delete")
