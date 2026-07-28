"""Health check endpoints."""

from flask import Blueprint, Response, jsonify

bp = Blueprint("health", __name__)


@bp.get("/health")
def health() -> Response:
    """Liveness probe — process is up."""
    return jsonify(status="ok")
