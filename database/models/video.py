import uuid

from sqlalchemy import TIMESTAMP, Column, Float, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.database import Base


class Video(Base):
    __tablename__ = "videos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    fps = Column(Float)
    duration = Column(Float)
    created_at = Column(TIMESTAMP, server_default=func.now())

    frames = relationship("Frame", back_populates="video", cascade="all, delete")
