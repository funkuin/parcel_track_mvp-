from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.parcel import (
    DashboardStatsResponse,
    ParcelCreate,
    ParcelResponse,
    ParcelStatusUpdate,
    ParcelTrackingResponse,
)
from app.services import parcel_service

router = APIRouter(prefix="/parcels", tags=["Parcels"])


@router.post(
    "",
    response_model=ParcelResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new parcel",
)
def register_parcel(
    parcel_in: ParcelCreate,
    db: Session = Depends(get_db),
):
    """Agency staff register a newly received parcel at the desk.

    The backend generates a unique tracking ID, sets status to REGISTERED,
    and records the initial milestone in status history.
    """
    return parcel_service.create_parcel(db, parcel_in)


@router.get(
    "",
    response_model=list[ParcelResponse],
    summary="List all parcels",
)
def list_parcels(
    db: Session = Depends(get_db),
):
    """Retrieve all parcels for the agency operator dashboard,

    ordered newest first.
    """
    return parcel_service.get_parcels(db)


# IMPORTANT: /stats/summary is registered BEFORE /{tracking_id}
# to prevent the tracking_id path parameter from capturing "stats".
@router.get(
    "/stats/summary",
    response_model=DashboardStatsResponse,
    summary="Dashboard summary statistics",
)
def get_dashboard_summary(
    db: Session = Depends(get_db),
):
    """Provide dashboard metrics: total count and counts per lifecycle status."""
    return parcel_service.get_dashboard_stats(db)


@router.patch(
    "/{tracking_id}/status",
    response_model=ParcelResponse,
    summary="Update parcel status",
)
def update_parcel_status(
    tracking_id: str,
    status_update: ParcelStatusUpdate,
    db: Session = Depends(get_db),
):
    """Agency staff update a parcel's status and append a milestone history note.

    Valid sequence: REGISTERED -> IN_TRANSIT -> ARRIVED -> COLLECTED.
    """
    try:
        return parcel_service.update_parcel_status(db, tracking_id, status_update)
    except parcel_service.ParcelNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Parcel with tracking ID '{tracking_id}' not found",
        )
    except parcel_service.InvalidStatusTransitionError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/{tracking_id}",
    response_model=ParcelTrackingResponse,
    summary="Public parcel tracking lookup",
)
def track_parcel(
    tracking_id: str,
    db: Session = Depends(get_db),
):
    """Public tracking lookup by tracking code.

    Customer-facing endpoint: does not require login and NEVER exposes
    sender/recipient phone numbers or names for privacy.
    """
    parcel = parcel_service.get_parcel_by_tracking_id(db, tracking_id)
    if not parcel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Parcel with tracking ID '{tracking_id}' not found",
        )
    return parcel
