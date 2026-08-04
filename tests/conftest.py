"""Shared pytest fixtures."""

from collections.abc import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app
from app.config import TestConfig
from app.extensions import db
from app.models import Room


@pytest.fixture
def app() -> Generator[Flask]:
    """Application bound to an in-memory SQLite database."""
    application = create_app(TestConfig)
    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """HTTP test client for the application."""
    return app.test_client()


@pytest.fixture
def room(app: Flask) -> Room:
    """Persist one active room for reservation tests."""
    assert app.testing
    active_room = Room(
        name="Test Room",
        capacity=6,
        description="Fixture room",
        is_active=True,
    )
    db.session.add(active_room)
    db.session.commit()
    return active_room
