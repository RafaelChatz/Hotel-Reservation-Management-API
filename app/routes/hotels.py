from flask import Blueprint, request, abort
from marshmallow import ValidationError
from http import HTTPStatus

from ..services.reservation import ReservationService
from ..services.hotel import HotelService
from ..models.reservation import Reservation
from ..schemas.hotel import hotel_schema, hotels_schema
from ..models.hotel import Hotel

hotels_bp = Blueprint('hotels', __name__, url_prefix='/hotels')

hotel_service = HotelService()
reservation_service = ReservationService()


@hotels_bp.route("/", methods=["GET"])
def get_hotels():
    """
    Get all hotels.
    ---
    tags:
      - Hotels
    responses:
        200:
            description: List of hotels.
    """
    hotels_list: list[Reservation] = hotel_service.get_all()
    return hotels_schema.dump(hotels_list)


@hotels_bp.route("/<int:hotel_id>", methods=["GET"])
def get_hotel(hotel_id):
    """
    Get hotel with hotel id.
    ---
    tags:
        - Hotels
    parameters:
        - in: path
          name: hotel_id
          type: integer
          required: true
          description: Hotel ID
    responses:
        200:
            description: Hotel.
        404:
            description: Hotel not found.
    """
    hotel: Reservation = hotel_service.get_or_404(hotel_id)
    return hotel_schema.dump(hotel)


@hotels_bp.route("/<int:hotel_id>", methods=["PUT"])
def update_hotel(hotel_id):
    """
    Update hotel with hotel id.
    ---
    tags:
        - Hotels
    consumes:
      - application/json
    parameters:
        - in: path
          name: hotel_id
          type: integer
          required: true
          description: Hotel ID
        - in: body
          name: body
          required: true
          schema:
            type: object
            required:
                - name
                - city
                - stars
            properties:
                name:
                    type: string
                    example: Hilton Athens
                city:
                    type: string
                    example: Athens
                stars:
                    type: integer
                    minimum: 1
                    maximum: 5
                    example: 5
    responses:
        200:
            description: Hotel updated.
        400:
            description: Bad request (wrong JSON input).
        404:
            description: Hotel not found.

    """
    try:
        data = hotel_schema.load(request.get_json())
    except ValidationError as err:
        abort(HTTPStatus.BAD_REQUEST, description=err.messages)

    hotel: Hotel = hotel_service.update(hotel_id, data)
    return hotel_schema.dump(hotel)


@hotels_bp.route("/<int:hotel_id>", methods=["DELETE"])
def delete_hotel(hotel_id):
    """
    Delete hotel with hotel id.
    ---
    tags:
        - Hotels
    parameters:
        - in: path
          name: hotel_id
          type: integer
          required: true
          description: Hotel ID
    responses:
        204:
            description: Hotel deleted no content.
        404:
            description: Hotel not found.

    """
    hotel_service.delete(hotel_id)
    reservation_service.cancel_all_with_hotel_id(hotel_id)
    return "", HTTPStatus.NO_CONTENT


@hotels_bp.route("/", methods=["POST"])
def create_hotel():
    """
    Create hotel.
    ---
    tags:
        - Hotels
    consumes:
        - application/json
    parameters:
        - in: body
          name: body
          required: true
          schema:
            type: object
            required:
                - name
                - city
                - stars
            properties:
                name:
                    type: string
                    example: Hilton Athens
                city:
                    type: string
                    example: Athens
                stars:
                    type: integer
                    minimum: 1
                    maximum: 5
                    example: 5
    responses:
        201:
            description: Hotel created.
        400:
            description: Bad request (wrong JSON input).
    """
    try:
        data = hotel_schema.load(request.get_json())
    except ValidationError as err:
        abort(HTTPStatus.BAD_REQUEST, description=err.messages)

    hotel: Hotel = hotel_service.create(data)
    return hotel_schema.dump(hotel), HTTPStatus.CREATED
