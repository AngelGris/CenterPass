import uuid

from sqlalchemy import TIMESTAMP, Column, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.database import Base


class Frame(Base):
    __tablename__ = "frames"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    video_id = Column(UUID(as_uuid=True), ForeignKey("videos.id", ondelete="CASCADE"))
    frame_number = Column(Integer)
    timestamp = Column(Float)
    filepath = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())

    video = relationship("Video", back_populates="frames")
