from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def home():
        return {
            "message": "Hello, Hotel Reservation API is running"
        }

    return app
