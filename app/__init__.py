from flask import Flask
from flasgger import Swagger
from .config import Config
from .extensions import db, migrate
from .models import register_models
from .routes import register_blueprints
from .errors import register_error_handlers


def create_app():
    app = Flask(__name__)

    # Configuration
    app.config.from_object(Config)
    swagger = Swagger(app)

    db.init_app(app)
    migrate.init_app(app, db)

    # Models
    register_models()

    # Blueprints
    register_blueprints(app)

    # Error Handling
    register_error_handlers(app)

    @app.route("/")
    def home():
        return {
            "message": "Hello, Hotel Reservation API is running"
        }

    return app
