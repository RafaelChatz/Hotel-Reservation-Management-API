from http import HTTPStatus


def register_error_handlers(app):
    @app.errorhandler(HTTPStatus.NOT_FOUND)
    def not_found(error):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND

    @app.errorhandler(HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
    def unsupported_media_type(error):
        return {
            "error": "Content-Type must be application/json"
        }, HTTPStatus.UNSUPPORTED_MEDIA_TYPE
