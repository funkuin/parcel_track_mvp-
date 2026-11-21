from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator


class ParcelStatus(str, Enum):
    """Allowed parcel lifecycle states."""
    REGISTERED = "REGISTERED"
    IN_TRANSIT = "IN_TRANSIT"
    ARRIVED = "ARRIVED"
    COLLECTED = "COLLECTED"


class ParcelCreate(BaseModel):
    """Schema for registering a new parcel at an agency desk."""
    model_config = ConfigDict(str_strip_whitespace=True)

    sender_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Full name of the sender",
        examples=["John Doe"],
    )
    sender_phone: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Contact telephone number of the sender",
        examples=["677123456"],
    )
    recipient_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Full name of the recipient",
        examples=["Mary Jane"],
    )
    recipient_phone: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Contact telephone number of the recipient",
        examples=["690123456"],
    )
    origin: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Origin branch / city",
        examples=["Douala"],
    )
    destination: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Destination branch / city",
        examples=["Bamenda"],
    )
    description: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Brief description of package contents",
        examples=["Box of clothes"],
    )


class ParcelStatusUpdate(BaseModel):
    """Schema for updating a parcel's status and appending an audit note."""
    model_config = ConfigDict(str_strip_whitespace=True)

    status: ParcelStatus = Field(
        ...,
        description="Target lifecycle status (REGISTERED, IN_TRANSIT, ARRIVED, COLLECTED)",
        examples=["IN_TRANSIT"],
    )
    note: Optional[str] = Field(
        default=None,
        max_length=250,
        description="Optional operational note explaining the transition",
        examples=["Parcel dispatched on morning coach from Douala"],
    )

    @field_validator("note")
    @classmethod
    def validate_note(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            trimmed = v.strip()
            if len(trimmed) == 0:
                raise ValueError("Note cannot be empty or whitespace only")
            return trimmed
        return None


class StatusHistoryResponse(BaseModel):
    """Schema for a milestone record in the parcel status audit trail."""
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    parcel_id: Optional[int] = None
    status: str
    note: Optional[str] = None
    timestamp: datetime


class ParcelResponse(BaseModel):
    """Agency-facing full parcel schema (includes contact details and internal ID)."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    tracking_id: str
    sender_name: str
    sender_phone: str
    recipient_name: str
    recipient_phone: str
    origin: str
    destination: str
    description: str
    status: str
    created_at: datetime
    updated_at: datetime
    status_history: list[StatusHistoryResponse] = []


class ParcelTrackingResponse(BaseModel):
    """Public customer-facing tracking response.

    Strict privacy safeguard: NEVER includes sender_name, sender_phone,
    recipient_name, recipient_phone, or internal database ID.
    """
    model_config = ConfigDict(from_attributes=True)

    tracking_id: str
    origin: str
    destination: str
    description: str
    status: str
    created_at: datetime
    updated_at: datetime
    status_history: list[StatusHistoryResponse] = []


class DashboardStatsResponse(BaseModel):
    """Aggregated status counts for the agency overview dashboard."""
    total: int
    registered: int
    in_transit: int
    arrived: int
    collected: int
