"""Admin panel routes."""

from flask import Blueprint, render_template

from app.decorators import admin_required

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.get("/")
@admin_required
def dashboard() -> str:
    """Admin landing page (full dashboard content in the next step)."""
    return render_template("admin/dashboard.html")
