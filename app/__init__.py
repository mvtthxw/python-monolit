"""Flask application package."""

from flask import Flask

from app.blueprints.health import bp as health_bp


def create_app() -> Flask:
    """Create the Flask application."""
    app = Flask(__name__)

    @app.get("/")
    def hello() -> str:
        return "Hello, World!"

    app.register_blueprint(health_bp)
    return app
