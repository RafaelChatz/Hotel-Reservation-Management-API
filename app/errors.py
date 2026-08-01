from http import HTTPStatus

from .messages import INVALID_REQUEST_BODY, INVALID_CONTENT_TYPE


def register_error_handlers(app):
    @app.errorhandler(HTTPStatus.NOT_FOUND)
    def not_found(error):
        return {"error": error.description}, HTTPStatus.NOT_FOUND

    @app.errorhandler(HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
    def unsupported_media_type(error):
        return {"error": INVALID_CONTENT_TYPE}, HTTPStatus.UNSUPPORTED_MEDIA_TYPE

    @app.errorhandler(HTTPStatus.CONFLICT)
    def conflict(error):
        return {"error": error.description}, HTTPStatus.CONFLICT

    @app.errorhandler(HTTPStatus.BAD_REQUEST)
    def bad_request(error):
        if "Failed to decode JSON object" in error.description:
            return {
                "errors": {
                    "json": [
                        INVALID_REQUEST_BODY
                    ]
                }
            }, HTTPStatus.BAD_REQUEST

        return {"errors": error.description}, HTTPStatus.BAD_REQUEST
