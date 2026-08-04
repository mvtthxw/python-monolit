"""Public HTML pages."""

from flask import Blueprint, render_template

from app.models import Reservation, ReservationStatus, Room

bp = Blueprint("main", __name__)


@bp.get("/")
def index() -> str:
    """Home page with rooms and reservations."""
    rooms = Room.query.filter_by(is_active=True).order_by(Room.name).all()
    reservations = Reservation.query.filter_by(status=ReservationStatus.CONFIRMED).order_by(Reservation.starts_at).all()
    return render_template(
        "index.html",
        rooms=rooms,
        reservations=reservations,
    )


@bp.get("/book")
def book() -> str:
    """Booking page placeholder until the WTForms step."""
    return render_template("book.html")
