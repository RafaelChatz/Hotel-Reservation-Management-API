def register_blueprints(app):
    from .hotels import hotels_bp
    from .customers import customers_bp
    from .reservations import reservations_bp

    app.register_blueprint(hotels_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(reservations_bp)
