"""Flask CLI commands."""

import os

import click
from flask import Flask
from werkzeug.security import generate_password_hash

from app.extensions import db
from app.models import Room, User

SEED_ROOMS: tuple[tuple[str, int, str], ...] = (
    ("Conference A", 8, "Small meeting room"),
    ("Conference B", 12, "Medium meeting room"),
    ("Conference C", 20, "Large conference hall"),
)


def register_cli(app: Flask) -> None:
    """Attach project CLI commands to the Flask app."""

    @app.cli.command("seed")
    def seed() -> None:
        """Seed admin user and sample rooms (idempotent)."""
        username = os.environ.get("ADMIN_USERNAME", "admin")
        password = os.environ.get("ADMIN_PASSWORD", "change-me")
        # ADMIN_EMAIL from .env is reserved until User gains an email field.

        user = User.query.filter_by(username=username).first()
        if user is None:
            user = User(
                username=username,
                password_hash=generate_password_hash(password),
                is_admin=True,
            )
            db.session.add(user)
            click.echo(f"Created admin user {username!r}")
        else:
            click.echo(f"Admin user {username!r} already exists — skipped")

        for name, capacity, description in SEED_ROOMS:
            room = Room.query.filter_by(name=name).first()
            if room is None:
                db.session.add(
                    Room(
                        name=name,
                        capacity=capacity,
                        description=description,
                        is_active=True,
                    ),
                )
                click.echo(f"Created room {name!r}")
            else:
                click.echo(f"Room {name!r} already exists — skipped")

        db.session.commit()
        click.echo("Seed complete.")
