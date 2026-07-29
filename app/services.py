"""Reservation domain services (collision checks and booking lifecycle)."""

from datetime import UTC, datetime

from app.extensions import db
from app.models import Reservation, ReservationStatus, Room


class ReservationError(Exception):
    """Base error for reservation operations."""


class InvalidReservationWindowError(ReservationError):
    """Raised when ends_at is not after starts_at."""


class RoomNotFoundError(ReservationError):
    """Raised when the target room does not exist."""


class RoomInactiveError(ReservationError):
    """Raised when the target room is not bookable."""


class ReservationConflictError(ReservationError):
    """Raised when the requested window overlaps an existing confirmed booking."""


class ReservationNotFoundError(ReservationError):
    """Raised when the reservation id does not exist."""


def _as_utc(value: datetime) -> datetime:
    """Normalize datetimes for comparison (SQLite often returns naive values)."""
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def intervals_overlap(
    starts_a: datetime,
    ends_a: datetime,
    starts_b: datetime,
    ends_b: datetime,
) -> bool:
    """Return True if two half-open windows [start, end) overlap."""
    starts_a = _as_utc(starts_a)
    ends_a = _as_utc(ends_a)
    starts_b = _as_utc(starts_b)
    ends_b = _as_utc(ends_b)
    return starts_a < ends_b and starts_b < ends_a


def has_conflict(
    room_id: int,
    starts_at: datetime,
    ends_at: datetime,
    *,
    exclude_reservation_id: int | None = None,
) -> bool:
    """Check whether a confirmed reservation on the room overlaps the window."""
    query = Reservation.query.filter_by(
        room_id=room_id,
        status=ReservationStatus.CONFIRMED,
    )
    if exclude_reservation_id is not None:
        query = query.filter(Reservation.id != exclude_reservation_id)

    return any(intervals_overlap(starts_at, ends_at, existing.starts_at, existing.ends_at) for existing in query)


def create_reservation(
    *,
    room_id: int,
    guest_name: str,
    guest_email: str,
    starts_at: datetime,
    ends_at: datetime,
) -> Reservation:
    """Create a confirmed reservation or raise a domain error."""
    if _as_utc(ends_at) <= _as_utc(starts_at):
        msg = "ends_at must be after starts_at"
        raise InvalidReservationWindowError(msg)

    room = db.session.get(Room, room_id)
    if room is None:
        raise RoomNotFoundError(room_id)
    if not room.is_active:
        raise RoomInactiveError(room_id)

    if has_conflict(room_id, starts_at, ends_at):
        raise ReservationConflictError(room_id)

    reservation = Reservation(
        room_id=room_id,
        guest_name=guest_name,
        guest_email=guest_email,
        starts_at=starts_at,
        ends_at=ends_at,
        status=ReservationStatus.CONFIRMED,
    )
    db.session.add(reservation)
    db.session.commit()
    return reservation


def cancel_reservation(reservation_id: int) -> Reservation:
    """Mark a reservation as cancelled."""
    reservation = db.session.get(Reservation, reservation_id)
    if reservation is None:
        raise ReservationNotFoundError(reservation_id)

    reservation.status = ReservationStatus.CANCELLED
    db.session.commit()
    return reservation
