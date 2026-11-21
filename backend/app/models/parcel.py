from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


def utc_now() -> datetime:
    """Return timezone-aware current UTC datetime."""
    return datetime.now(timezone.utc)


class Parcel(Base):
    __tablename__ = "parcels"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tracking_id = Column(String(30), unique=True, index=True, nullable=False)
    sender_name = Column(String(100), nullable=False)
    sender_phone = Column(String(20), nullable=False)
    recipient_name = Column(String(100), nullable=False)
    recipient_phone = Column(String(20), nullable=False)
    origin = Column(String(50), nullable=False)
    destination = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)
    status = Column(String(20), default="REGISTERED", index=True, nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(
        DateTime,
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )

    # One-to-many relationship: One parcel has many status history records
    status_history = relationship(
        "ParcelStatusHistory",
        back_populates="parcel",
        cascade="all, delete-orphan",
        order_by="ParcelStatusHistory.timestamp.asc()",
    )
