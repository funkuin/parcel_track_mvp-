from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.parcel import Parcel
from app.models.parcel_status_history import ParcelStatusHistory
from app.schemas.parcel import ParcelCreate, ParcelStatusUpdate
from app.services.tracking_service import generate_unique_tracking_id


def utc_now() -> datetime:
    """Return timezone-aware current UTC datetime."""
    return datetime.now(timezone.utc)


class ParcelNotFoundError(Exception):
    """Raised when a parcel cannot be found by its tracking ID."""
    pass


class InvalidStatusTransitionError(Exception):
    """Raised when a status transition violates the lifecycle sequence."""
    pass


# Ordered lifecycle stages
STATUS_LIFECYCLE = ["REGISTERED", "IN_TRANSIT", "ARRIVED", "COLLECTED"]

# Allowed forward single-step transitions
VALID_TRANSITIONS = {
    "REGISTERED": "IN_TRANSIT",
    "IN_TRANSIT": "ARRIVED",
    "ARRIVED": "COLLECTED",
}


def create_parcel(db: Session, parcel_in: ParcelCreate) -> Parcel:
    """Register a new parcel and create its initial status history milestone

    in a single database transaction.
    """
    # Generate unique backend tracking identifier
    tracking_id = generate_unique_tracking_id(db, parcel_in.destination)
    now = utc_now()

    # Instantiate parcel with default status REGISTERED
    parcel = Parcel(
        tracking_id=tracking_id,
        sender_name=parcel_in.sender_name,
        sender_phone=parcel_in.sender_phone,
        recipient_name=parcel_in.recipient_name,
        recipient_phone=parcel_in.recipient_phone,
        origin=parcel_in.origin,
        destination=parcel_in.destination,
        description=parcel_in.description,
        status="REGISTERED",
        created_at=now,
        updated_at=now,
    )

    # Initial status history milestone
    initial_history = ParcelStatusHistory(
        status="REGISTERED",
        note="Parcel registered at agency",
        timestamp=now,
    )
    parcel.status_history.append(initial_history)

    # Commit both entities atomically
    try:
        db.add(parcel)
        db.commit()
        db.refresh(parcel)
        return parcel
    except Exception:
        db.rollback()
        raise


def get_parcels(db: Session) -> list[Parcel]:
    """Retrieve all parcels for agency dashboard, ordered newest first."""
    return db.query(Parcel).order_by(Parcel.created_at.desc()).all()


def get_parcel_by_tracking_id(db: Session, tracking_id: str) -> Optional[Parcel]:
    """Look up a parcel by its unique tracking code."""
    normalized_id = tracking_id.strip().upper()
    return db.query(Parcel).filter(Parcel.tracking_id == normalized_id).first()


def update_parcel_status(
    db: Session, tracking_id: str, update_in: ParcelStatusUpdate
) -> Parcel:
    """Validate and transition a parcel's status, appending a new audit history record.

    Enforces the forward sequence: REGISTERED -> IN_TRANSIT -> ARRIVED -> COLLECTED.
    """
    parcel = get_parcel_by_tracking_id(db, tracking_id)
    if not parcel:
        raise ParcelNotFoundError(
            f"Parcel with tracking ID '{tracking_id}' not found"
        )

    current_status = parcel.status
    target_status = (
        update_in.status.value
        if hasattr(update_in.status, "value")
        else str(update_in.status)
    )

    # 1. Prevent updates to terminal COLLECTED state
    if current_status == "COLLECTED":
        raise InvalidStatusTransitionError(
            f"Parcel '{parcel.tracking_id}' is already COLLECTED and cannot be updated further."
        )

    # 2. Prevent repeating the current status
    if current_status == target_status:
        raise InvalidStatusTransitionError(
            f"Parcel '{parcel.tracking_id}' is already in '{current_status}' status."
        )

    # 3. Prevent reverting to an earlier status
    current_idx = (
        STATUS_LIFECYCLE.index(current_status)
        if current_status in STATUS_LIFECYCLE
        else -1
    )
    target_idx = (
        STATUS_LIFECYCLE.index(target_status)
        if target_status in STATUS_LIFECYCLE
        else -1
    )

    if target_idx < current_idx:
        raise InvalidStatusTransitionError(
            f"Cannot revert parcel status from '{current_status}' to '{target_status}'."
        )

    # 4. Prevent skipping statuses
    expected_next = VALID_TRANSITIONS.get(current_status)
    if target_status != expected_next:
        raise InvalidStatusTransitionError(
            f"Cannot transition directly from '{current_status}' to '{target_status}'. Expected '{expected_next}'."
        )

    # Apply update and append history record atomically
    now = utc_now()
    parcel.status = target_status
    parcel.updated_at = now

    new_history = ParcelStatusHistory(
        status=target_status,
        note=update_in.note,
        timestamp=now,
    )
    parcel.status_history.append(new_history)

    try:
        db.commit()
        db.refresh(parcel)
        return parcel
    except Exception:
        db.rollback()
        raise


def get_dashboard_stats(db: Session) -> dict:
    """Compute summary counts for agency dashboard metric cards."""
    total = db.query(func.count(Parcel.id)).scalar() or 0

    # Group counts by current status
    counts = dict(
        db.query(Parcel.status, func.count(Parcel.id))
        .group_by(Parcel.status)
        .all()
    )

    return {
        "total": total,
        "registered": counts.get("REGISTERED", 0),
        "in_transit": counts.get("IN_TRANSIT", 0),
        "arrived": counts.get("ARRIVED", 0),
        "collected": counts.get("COLLECTED", 0),
    }
