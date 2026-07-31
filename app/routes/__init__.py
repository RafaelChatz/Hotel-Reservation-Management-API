def register_blueprints(app):
    from .hotels import hotels_bp

    app.register_blueprint(hotels_bp)