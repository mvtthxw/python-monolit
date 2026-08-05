"""Admin panel routes."""

from flask import Blueprint, render_template

from app.decorators import admin_required
from app.models import Reservation, Room

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.get("/")
@admin_required
def dashboard() -> str:
    """Admin overview of all rooms and reservations."""
    rooms = Room.query.order_by(Room.name).all()
    reservations = Reservation.query.order_by(Reservation.starts_at.desc()).all()
    return render_template(
        "admin/dashboard.html",
        rooms=rooms,
        reservations=reservations,
    )
