from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text
from sqlalchemy.sql import func

from app.db.database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String, nullable=False)

    predicted_class = Column(String, nullable=False)

    confidence = Column(Float, nullable=False)

    probabilities_json = Column(Text, nullable=False)

    model_version = Column(String, nullable=False)

    latency_ms = Column(Float, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    image_width = Column(Integer, nullable=False)

    image_height = Column(Integer, nullable=False)

    file_size_kb = Column(Float, nullable=False)

    review_status = Column(
        String,
        default="pending_review"
    )

    low_confidence_flag = Column(
        Boolean,
        default=False
    )

    notes = Column(Text, nullable=True)

    true_label = Column(Text, nullable=True)

    correct = Column(Boolean, nullable=True)