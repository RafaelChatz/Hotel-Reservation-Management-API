from flask import Flask

from .config import Config
from .extensions import db, migrate
from .models import register_models


def create_app():
    app = Flask(__name__)

    # Configuration
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Models
    register_models()

    @app.route("/")
    def home():
        return {
            "message": "Hello, Hotel Reservation API is running"
        }

    return app
