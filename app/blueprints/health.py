"""Health and readiness check endpoints."""

from flask import Blueprint, Response, jsonify
from sqlalchemy import text

from app.extensions import db

bp = Blueprint("health", __name__)


@bp.get("/health")
def health() -> Response:
    """Liveness probe — process is up."""
    return jsonify(status="ok")


@bp.get("/ready")
def ready() -> tuple[Response, int]:
    """Readiness probe — database connection works."""
    try:
        db.session.execute(text("SELECT 1"))
    except Exception:  # noqa: BLE001 - probe must not leak internals
        return jsonify(status="unavailable"), 503
    return jsonify(status="ok"), 200
