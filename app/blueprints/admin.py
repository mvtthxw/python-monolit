"""Admin panel routes."""

from flask import Blueprint, Response, abort, flash, redirect, render_template, url_for
from sqlalchemy.exc import IntegrityError

from app.decorators import admin_required
from app.extensions import db
from app.forms import RoomForm
from app.models import Reservation, Room
from app.services import ReservationNotFoundError, cancel_reservation

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


@bp.route("/rooms/new", methods=["GET", "POST"])
@admin_required
def room_create() -> str | Response:
    """Create a new room."""
    form = RoomForm()
    if form.validate_on_submit():
        room = Room(
            name=form.name.data or "",
            capacity=form.capacity.data or 1,
            description=form.description.data or None,
            is_active=bool(form.is_active.data),
        )
        db.session.add(room)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("A room with that name already exists.", "error")
        else:
            flash(f"Room {room.name!r} created.", "success")
            return redirect(url_for("admin.dashboard"))
    return render_template("admin/room_form.html", form=form, title="New room")


@bp.route("/rooms/<int:room_id>/edit", methods=["GET", "POST"])
@admin_required
def room_edit(room_id: int) -> str | Response:
    """Edit an existing room."""
    room = db.session.get(Room, room_id)
    if room is None:
        abort(404)

    form = RoomForm(obj=room)
    if form.validate_on_submit():
        room.name = form.name.data or room.name
        room.capacity = form.capacity.data or room.capacity
        room.description = form.description.data or None
        room.is_active = bool(form.is_active.data)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("A room with that name already exists.", "error")
        else:
            flash(f"Room {room.name!r} updated.", "success")
            return redirect(url_for("admin.dashboard"))
    return render_template(
        "admin/room_form.html",
        form=form,
        title=f"Edit {room.name}",
    )


@bp.post("/reservations/<int:reservation_id>/cancel")
@admin_required
def reservation_cancel(reservation_id: int) -> Response:
    """Cancel a confirmed reservation via the domain service."""
    try:
        reservation = cancel_reservation(reservation_id)
    except ReservationNotFoundError:
        abort(404)

    flash(
        f"Reservation #{reservation.id} for {reservation.room.name} cancelled.",
        "success",
    )
    return redirect(url_for("admin.dashboard"))
