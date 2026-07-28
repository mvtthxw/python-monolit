"""Database models."""

from datetime import UTC, datetime
from enum import StrEnum

from flask_login import UserMixin
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db, login_manager


class ReservationStatus(StrEnum):
    """Lifecycle status of a reservation."""

    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class User(UserMixin, db.Model):
    """Application user (admin accounts for now)."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(default=False)


class Room(db.Model):
    """Bookable meeting room."""

    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    capacity: Mapped[int]
    description: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(default=True)

    reservations: Mapped[list["Reservation"]] = relationship(back_populates="room")


class Reservation(db.Model):
    """Guest booking for a room in a time window."""

    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    guest_name: Mapped[str]
    guest_email: Mapped[str]
    starts_at: Mapped[datetime]
    ends_at: Mapped[datetime]
    status: Mapped[str] = mapped_column(default=ReservationStatus.CONFIRMED)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    room: Mapped["Room"] = relationship(back_populates="reservations")


@login_manager.user_loader
def load_user(user_id: str) -> User | None:
    """Resolve the current user from the session user id."""
    return db.session.get(User, int(user_id))
