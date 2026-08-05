"""Authentication routes (login / logout)."""

from flask import Blueprint, Response, flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash

from app.forms import LoginForm
from app.models import User

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login() -> str | Response:
    """Log in an admin user."""
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        password = form.password.data or ""
        if user is not None and user.is_admin and check_password_hash(user.password_hash, password):
            login_user(user)
            flash("Logged in.", "success")
            return redirect(url_for("admin.dashboard"))
        flash("Invalid username or password.", "error")

    return render_template("auth/login.html", form=form)


@bp.post("/logout")
def logout() -> Response:
    """Log out the current user."""
    logout_user()
    flash("Logged out.", "success")
    return redirect(url_for("main.index"))
