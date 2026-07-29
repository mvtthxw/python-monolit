"""Flask application package."""

from dotenv import load_dotenv
from flask import Flask

from app import models as _models  # noqa: F401  # register models with metadata
from app.blueprints.health import bp as health_bp
from app.blueprints.reservations import bp as reservations_bp
from app.blueprints.rooms import bp as rooms_bp
from app.extensions import csrf, db, login_manager, migrate


def create_app(config_object: str = "app.config.Config") -> Flask:
    """Create and configure the Flask application."""
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    @app.get("/")
    def hello() -> str:
        return "Hello, World!"

    app.register_blueprint(health_bp)
    app.register_blueprint(rooms_bp)
    app.register_blueprint(reservations_bp)
    csrf.exempt(reservations_bp)
    return app
