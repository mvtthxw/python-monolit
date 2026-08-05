"""Auth helpers."""

from collections.abc import Callable
from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user, login_required


def admin_required(view: Callable[..., object]) -> Callable[..., object]:
    """Require a logged-in admin user."""

    @wraps(view)
    @login_required
    def wrapped(*args: object, **kwargs: object) -> object:
        if not current_user.is_admin:
            flash("Admin access required.", "error")
            return redirect(url_for("main.index"))
        return view(*args, **kwargs)

    return wrapped
