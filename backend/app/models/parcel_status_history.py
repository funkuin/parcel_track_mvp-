from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


def utc_now() -> datetime:
    """Return timezone-aware current UTC datetime."""
    return datetime.now(timezone.utc)


class ParcelStatusHistory(Base):
    __tablename__ = "parcel_status_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    parcel_id = Column(
        Integer,
        ForeignKey("parcels.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status = Column(String(20), nullable=False)
    note = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=utc_now, nullable=False, index=True)

    # Reverse relationship back to parent parcel
    parcel = relationship("Parcel", back_populates="status_history")
