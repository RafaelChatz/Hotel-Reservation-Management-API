from flask import Blueprint, request, abort
from marshmallow import ValidationError
from http import HTTPStatus

from ..messages import HOTEL_NOT_FOUND
from ..schemas.hotel import hotel_schema, hotels_schema
from ..extensions import db
from ..models.hotel import Hotel

hotels_bp = Blueprint('hotels', __name__, url_prefix='/hotels')


def get_hotel_or_404(hotel_id) -> Hotel:
    hotel: Hotel = db.session.get(Hotel, hotel_id)
    if hotel is None:
        abort(HTTPStatus.NOT_FOUND, description=HOTEL_NOT_FOUND)
    return hotel


@hotels_bp.route("/", methods=["GET"])
def get_hotels():
    hotels_list: list[Hotel] = db.session.query(Hotel).all()
    return hotels_schema.dump(hotels_list)


@hotels_bp.route("/<int:hotel_id>", methods=["GET"])
def get_hotel(hotel_id):
    hotel: Hotel = get_hotel_or_404(hotel_id)
    return hotel_schema.dump(hotel)


@hotels_bp.route("/<int:hotel_id>", methods=["PUT"])
def update_hotel(hotel_id):
    hotel: Hotel = get_hotel_or_404(hotel_id)

    try:
        data = hotel_schema.load(request.get_json())
    except ValidationError as err:
        abort(HTTPStatus.BAD_REQUEST, description=err.messages)

    hotel.name = data["name"]
    hotel.city = data["city"]
    hotel.stars = data["stars"]

    db.session.commit()
    return hotel_schema.dump(hotel)


@hotels_bp.route("/", methods=["POST"])
def create_hotel():
    try:
        data = hotel_schema.load(request.get_json())
    except ValidationError as err:
        abort(HTTPStatus.BAD_REQUEST, description=err.messages)

    hotel = Hotel(name=data["name"], city=data["city"], stars=data["stars"])
    db.session.add(hotel)
    db.session.commit()
    return hotel_schema.dump(hotel), HTTPStatus.CREATED
