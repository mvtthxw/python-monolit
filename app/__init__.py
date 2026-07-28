"""Flask application package."""

from flask import Flask


def create_app() -> Flask:
    """Create the Flask application."""
    app = Flask(__name__)

    @app.get("/")
    def hello() -> str:
        return "Hello, World!"

    return app
