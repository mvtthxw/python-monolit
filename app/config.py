"""Application configuration loaded from environment variables."""

import os
from typing import Any, ClassVar

from sqlalchemy.pool import StaticPool


class Config:
    """Default application settings."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///app.db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    """In-memory SQLite settings for automated tests."""

    TESTING = True
    SECRET_KEY = "test-secret"  # noqa: S105 - test-only key
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_ENGINE_OPTIONS: ClassVar[dict[str, Any]] = {
        "connect_args": {"check_same_thread": False},
        "poolclass": StaticPool,
    }
    WTF_CSRF_ENABLED = False
