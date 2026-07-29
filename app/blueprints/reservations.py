"""Reservations API endpoints."""

from datetime import datetime
from typing import Any, cast

from flask import Blueprint, Response, jsonify, request

from app.models import Reservation
from app.services import (
    InvalidReservationWindowError,
    ReservationConflictError,
    RoomInactiveError,
    RoomNotFoundError,
    create_reservation,
)

bp = Blueprint("reservations_api", __name__, url_prefix="/api")

CreateFields = tuple[int, str, str, datetime, datetime]
ErrorResponse = tuple[Response, int]


def _reservation_to_dict(reservation: Reservation) -> dict[str, Any]:
    """Serialize a reservation for JSON responses."""
    return {
        "id": reservation.id,
        "room_id": reservation.room_id,
        "guest_name": reservation.guest_name,
        "guest_email": reservation.guest_email,
        "starts_at": reservation.starts_at.isoformat(),
        "ends_at": reservation.ends_at.isoformat(),
        "status": reservation.status,
        "created_at": reservation.created_at.isoformat(),
    }


def _parse_datetime(value: object, field: str) -> datetime:
    """Parse an ISO-8601 datetime string from JSON."""
    if not isinstance(value, str) or not value:
        msg = f"{field} must be an ISO-8601 datetime string"
        raise ValueError(msg)
    normalized = value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized)


def _parse_create_payload(payload: dict[str, Any]) -> CreateFields | ErrorResponse:
    """Validate POST body; return fields or an error response."""
    required = ("room_id", "guest_name", "guest_email", "starts_at", "ends_at")
    missing = [key for key in required if key not in payload]
    if missing:
        return jsonify(error=f"missing fields: {', '.join(missing)}"), 400

    try:
        room_id = int(payload["room_id"])
        guest_name = str(payload["guest_name"]).strip()
        guest_email = str(payload["guest_email"]).strip()
        starts_at = _parse_datetime(payload["starts_at"], "starts_at")
        ends_at = _parse_datetime(payload["ends_at"], "ends_at")
    except (TypeError, ValueError) as exc:
        return jsonify(error=str(exc)), 400

    if not guest_name or not guest_email:
        return jsonify(error="guest_name and guest_email are required"), 400

    return room_id, guest_name, guest_email, starts_at, ends_at


@bp.get("/reservations")
def list_reservations() -> Response:
    """Return reservations as JSON."""
    reservations = Reservation.query.order_by(Reservation.starts_at).all()
    return jsonify([_reservation_to_dict(item) for item in reservations])


@bp.post("/reservations")
def post_reservation() -> tuple[Response, int]:
    """Create a reservation; conflicts return HTTP 409."""
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(error="JSON body required"), 400

    parsed = _parse_create_payload(payload)
    if isinstance(parsed[0], Response):
        return cast("ErrorResponse", parsed)

    room_id, guest_name, guest_email, starts_at, ends_at = cast("CreateFields", parsed)

    try:
        reservation = create_reservation(
            room_id=room_id,
            guest_name=guest_name,
            guest_email=guest_email,
            starts_at=starts_at,
            ends_at=ends_at,
        )
    except InvalidReservationWindowError as exc:
        return jsonify(error=str(exc)), 400
    except (RoomNotFoundError, RoomInactiveError) as exc:
        return jsonify(error=str(exc)), 404
    except ReservationConflictError:
        return jsonify(error="reservation conflict"), 409

    return jsonify(_reservation_to_dict(reservation)), 201
