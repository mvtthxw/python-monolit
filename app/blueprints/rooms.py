"""Rooms API endpoints."""

from flask import Blueprint, Response, jsonify

from app.models import Room

bp = Blueprint("rooms_api", __name__, url_prefix="/api")


@bp.get("/rooms")
def list_rooms() -> Response:
    """Return active rooms as JSON."""
    rooms = Room.query.filter_by(is_active=True).order_by(Room.name).all()
    return jsonify(
        [
            {
                "id": room.id,
                "name": room.name,
                "capacity": room.capacity,
                "description": room.description,
            }
            for room in rooms
        ],
    )
