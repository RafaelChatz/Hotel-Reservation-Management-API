from flask import Flask
from .config import Config
from .extensions import db, migrate


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from .models.hotel import Hotel
    from .models.customer import Customer
    from .models.reservation import Reservation

    @app.route("/")
    def home():
        return {
            "message": "Hello, Hotel Reservation API is running"
        }

    return app
