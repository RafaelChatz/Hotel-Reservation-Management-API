from flask import Blueprint, request, abort
from marshmallow import ValidationError
from http import HTTPStatus
from datetime import datetime

from ..messages import HOTEL_NOT_FOUND, CUSTOMER_NOT_FOUND, RESERVATION_NOT_FOUND, CUSTOMER_HAS_OVERLAPPING_RESERVATION
from ..models.hotel import Hotel
from ..models.customer import Customer
from ..models.reservation import Reservation, StatusType
from ..schemas.reservation import reservation_schema, reservations_schema
from ..extensions import db

reservations_bp = Blueprint('reservations', __name__, url_prefix='/reservations')


def get_reservation_or_404(reservation_id) -> Reservation:
    reservation: Reservation = db.session.get(Reservation, reservation_id)
    if reservation is None:
        abort(HTTPStatus.NOT_FOUND, description=RESERVATION_NOT_FOUND)
    return reservation


def validate_hotel_exists(hotel_id):
    if db.session.get(Hotel, hotel_id) is None:
        abort(HTTPStatus.NOT_FOUND, description=HOTEL_NOT_FOUND)


def validate_customer_exists(customer_id):
    if db.session.get(Customer, customer_id) is None:
        abort(HTTPStatus.NOT_FOUND, description=CUSTOMER_NOT_FOUND)


def query_reservations(filters) -> list[Reservation]:
    query = (db.session.query(Reservation)
             .join(Customer, Reservation.customer_id == Customer.id)
             .join(Hotel, Reservation.hotel_id == Hotel.id))

    if filters.get("hotel_name"):
        query = query.filter(Hotel.name.ilike(f"%{filters['hotel_name']}%"))

    if filters.get("customer_name"):
        full_name = Customer.first_name + " " + Customer.last_name
        query = query.filter(full_name.ilike(f"%{filters['customer_name']}%"))

    if filters.get("city"):
        query = query.filter(Hotel.city.ilike(f"%{filters['city']}%"))

    if filters.get("status"):
        query = query.filter(Reservation.status == StatusType[filters["status"]])

    if filters.get("check_in"):
        check_in = datetime.strptime(filters["check_in"], "%Y-%m-%d").date()
        query = query.filter(Reservation.check_in >= check_in)

    if filters.get("check_out"):
        check_out = datetime.strptime(filters["check_out"], "%Y-%m-%d").date()
        query = query.filter(Reservation.check_out <= check_out)

    return query.distinct()


def validate_no_overlapping_reservations(customer_id, check_in, check_out):
    reservation = (
        db.session.query(Reservation)
        .filter(
            Reservation.customer_id == customer_id,
            Reservation.status == StatusType.ACTIVE,
            Reservation.check_in <= check_out,
            Reservation.check_out >= check_in,
        )
        .first()
    )

    if reservation:
        abort(HTTPStatus.CONFLICT, description=CUSTOMER_HAS_OVERLAPPING_RESERVATION)


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

    reservations = query_reservations(filters)

    return reservations_schema.dump(reservations)


@reservations_bp.route("/", methods=["GET"])
def get_reservations():
    reservations_list: list[Reservation] = db.session.query(Reservation).all()
    return reservations_schema.dump(reservations_list)


@reservations_bp.route("/<int:reservation_id>", methods=["GET"])
def get_reservation(reservation_id):
    reservation: Reservation = get_reservation_or_404(reservation_id)
    return reservation_schema.dump(reservation)


@reservations_bp.route("/<int:reservation_id>", methods=["DELETE"])
def delete_reservation(reservation_id):
    reservation: Reservation = get_reservation_or_404(reservation_id)
    reservation.status = StatusType.CANCELLED  # idempotent no need to check if already canceled

    db.session.commit()
    return "", HTTPStatus.NO_CONTENT


@reservations_bp.route("/", methods=["POST"])
def create_reservation():
    try:
        data = reservation_schema.load(request.get_json())
    except ValidationError as err:
        abort(HTTPStatus.BAD_REQUEST, description=err.messages)

    validate_hotel_exists(data["hotel_id"])
    validate_customer_exists(data["customer_id"])
    validate_no_overlapping_reservations(data["customer_id"], data["check_in"], data["check_out"])

    reservation = Reservation(hotel_id=data["hotel_id"],
                              customer_id=data["customer_id"],
                              check_in=data["check_in"],
                              check_out=data["check_out"],
                              total_price=data["total_price"],
                              status=data['status'])

    db.session.add(reservation)
    db.session.commit()
    return reservation_schema.dump(reservation), HTTPStatus.CREATED
