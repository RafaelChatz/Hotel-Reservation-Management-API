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
    reservations_list: list[Reservation] = reservation_service.get_all()
    return reservations_schema.dump(reservations_list)


@reservations_bp.route("/<int:reservation_id>", methods=["GET"])
def get_reservation(reservation_id):
    reservation: Reservation = reservation_service.get_or_404(reservation_id)
    return reservation_schema.dump(reservation)


@reservations_bp.route("/<int:reservation_id>", methods=["DELETE"])
def cancel_reservation(reservation_id):
    reservation_service.cancel(reservation_id)
    return "", HTTPStatus.NO_CONTENT


@reservations_bp.route("/", methods=["POST"])
def create_reservation():
    try:
        data = reservation_schema.load(request.get_json())
    except ValidationError as err:
        abort(HTTPStatus.BAD_REQUEST, description=err.messages)

    reservation: Reservation = reservation_service.create(data)
    return reservation_schema.dump(reservation), HTTPStatus.CREATED
