"""Public HTML pages."""

from flask import Blueprint, render_template

bp = Blueprint("main", __name__)


@bp.get("/")
def index() -> str:
    """Home page shell (content lists land in the next step)."""
    return render_template("index.html")


@bp.get("/book")
def book() -> str:
    """Booking page placeholder until the WTForms step."""
    return render_template("book.html")
