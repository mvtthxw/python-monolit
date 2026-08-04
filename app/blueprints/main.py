"""Public HTML pages."""

from flask import Blueprint, Response, flash, redirect, render_template, url_for

from app.forms import BookingForm
from app.models import Reservation, ReservationStatus, Room
from app.services import (
    InvalidReservationWindowError,
    ReservationConflictError,
    RoomInactiveError,
    RoomNotFoundError,
    create_reservation,
)

bp = Blueprint("main", __name__)


def _room_choices() -> list[tuple[int, str]]:
    """Active rooms for the booking select field."""
    rooms = Room.query.filter_by(is_active=True).order_by(Room.name).all()
    return [(room.id, f"{room.name} (capacity {room.capacity})") for room in rooms]


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


@bp.route("/book", methods=["GET", "POST"])
def book() -> str | Response:
    """Show and handle the public booking form."""
    form = BookingForm()
    form.room_id.choices = _room_choices()

    if form.validate_on_submit():
        try:
            create_reservation(
                room_id=form.room_id.data,
                guest_name=form.guest_name.data or "",
                guest_email=form.guest_email.data or "",
                starts_at=form.starts_at.data,
                ends_at=form.ends_at.data,
            )
        except InvalidReservationWindowError:
            flash("End time must be after start time.", "error")
        except (RoomNotFoundError, RoomInactiveError):
            flash("That room is not available.", "error")
        except ReservationConflictError:
            flash("That time slot conflicts with an existing reservation.", "error")
        else:
            flash("Reservation confirmed.", "success")
            return redirect(url_for("main.index"))

    return render_template("book.html", form=form)
