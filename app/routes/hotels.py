from flask import Blueprint, jsonify, request, abort
from marshmallow import ValidationError
from http import HTTPStatus

from ..schemas.hotel import hotel_schema, hotels_schema
from ..extensions import db
from ..models.hotel import Hotel

hotels_bp = Blueprint('hotels', __name__, url_prefix='/hotels')


@hotels_bp.route("/", methods=["GET"])
def get_hotels():
    hotels_list: list[Hotel] = db.session.query(Hotel).all()
    return hotels_schema.dump(hotels_list)


@hotels_bp.route("/<int:id>", methods=["GET"])
def get_hotel(id):
    hotel: Hotel = db.session.get(Hotel, id)
    if hotel is None:
        abort(HTTPStatus.NOT_FOUND)
    return hotel_schema.dump(hotel)


@hotels_bp.route("/<int:id>", methods=["PUT"])
def update_hotel(id):
    hotel: Hotel = db.session.get(Hotel, id)
    if hotel is None:
        abort(HTTPStatus.NOT_FOUND)

    try:
        data = hotel_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), HTTPStatus.BAD_REQUEST

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
        return jsonify(err.messages), HTTPStatus.BAD_REQUEST

    hotel = Hotel(name=data["name"], city=data["city"], stars=data["stars"])
    db.session.add(hotel)
    db.session.commit()
    return hotel_schema.dump(hotel), HTTPStatus.CREATED
