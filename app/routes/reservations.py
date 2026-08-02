from flask import Blueprint, request, abort
from marshmallow import ValidationError
from http import HTTPStatus

from ..services.reservation import ReservationService
from ..models.reservation import Reservation
from ..schemas.reservation import reservation_schema, reservations_schema

reservations_bp = Blueprint('reservations', __name__, url_prefix='/reservations')

reservation_service = ReservationService()


@reservations_bp.route("/search", methods=["GET"])
def search_reservations():
    """
    Search reservations.
    ---
    tags:
      - Reservations
    parameters:
        - in: query
          name: hotelName
          type: string
          required: false
          description: Hotel name.
          example: Hilton Athens

        - in: query
          name: customerName
          type: string
          required: false
          description: Customer's full name.
          example: John Doe

        - in: query
          name: city
          type: string
          required: false
          description: Hotel city.
          example: Athens

        - in: query
          name: status
          type: string
          required: false
          description: Reservation status.
          enum:
           - ACTIVE
           - CANCELLED
          example: ACTIVE

        - in: query
          name: checkIn
          type: string
          format: date
          required: false
          description: Return reservations with check-in date on or after this date.
          example: "2027-11-10"

        - in: query
          name: checkOut
          type: string
          format: date
          required: false
          description: Return reservations with check-out date on or before this date.
          example: "2027-11-15"

    responses:
        200:
            description: List of reservations matching the supplied filters.
        400:
            description: Invalid search parameters.
    """
    filters = {
        "hotel_name": request.args.get("hotelName"),
        "customer_name": request.args.get("customerName"),
        "city": request.args.get("city"),
        "status": request.args.get("status"),
        "check_in": request.args.get("checkIn"),
        "check_out": request.args.get("checkOut"),
    }

    reservations = reservation_service.search(filters)
    return reservations_schema.dump(reservations)


@reservations_bp.route("/", methods=["GET"])
def get_reservations():
    """
    Get all reservations.
    ---
    tags:
      - Reservations
    responses:
        200:
            description: List of reservations.
    """
    reservations_list: list[Reservation] = reservation_service.get_all()
    return reservations_schema.dump(reservations_list)


@reservations_bp.route("/<int:reservation_id>", methods=["GET"])
def get_reservation(reservation_id):
    """
    Get reservation with reservation id.
    ---
    tags:
        - Reservations
    parameters:
        - in: path
          name: reservation_id
          type: integer
          required: true
          description: Reservation ID
    responses:
        200:
            description: Reservation.
        404:
            description: Reservation not found.
    """
    reservation: Reservation = reservation_service.get_or_404(reservation_id)
    return reservation_schema.dump(reservation)


@reservations_bp.route("/<int:reservation_id>", methods=["DELETE"])
def cancel_reservation(reservation_id):
    """
    Delete reservation with reservation id.
    ---
    tags:
        - Reservations
    parameters:
        - in: path
          name: reservation_id
          type: integer
          required: true
          description: Reservation ID
    responses:
        204:
            description: Reservation cancelled no content.
        404:
            description: Reservation not found.
    """
    reservation_service.cancel(reservation_id)
    return "", HTTPStatus.NO_CONTENT


@reservations_bp.route("/", methods=["POST"])
def create_reservation():
    """
    Create reservation.
    ---
    tags:
        - Reservations
    consumes:
        - application/json
    parameters:
        - in: body
          name: body
          required: true
          schema:
            type: object
            required:
                - hotel_id
                - customer_id
                - check_in
                - check_out
                - total_price
                - status
            properties:
                hotel_id:
                    type: integer
                    example: 12
                customer_id:
                    type: integer
                    example: 25
                check_in:
                    type: string
                    format: date
                    example: "2027-11-10"
                check_out:
                    type: string
                    format: date
                    example: "2027-11-15"
                total_price:
                    type: number
                    format: double
                    example: 125.00
                status:
                    type: string
                    example: ACTIVE
    responses:
        201:
            description: Reservation created.
        400:
            description: Bad request (wrong JSON input).
        409:
            description: Conflict overlapping reservations.
    """
    try:
        data = reservation_schema.load(request.get_json())
    except ValidationError as err:
        abort(HTTPStatus.BAD_REQUEST, description=err.messages)

    reservation: Reservation = reservation_service.create(data)
    return reservation_schema.dump(reservation), HTTPStatus.CREATED
