from http import HTTPStatus
from flask import abort
from datetime import datetime, timezone

from ..models.hotel import Hotel
from ..messages import HOTEL_NOT_FOUND
from ..repositories.hotel import HotelRepository


class HotelService:
    def __init__(self):
        self.hotel_repository = HotelRepository()

    def get_all(self):
        return self.hotel_repository.get_all()

    def get_or_404(self, hotel_id) -> Hotel:
        hotel: Hotel = self.hotel_repository.get_by_id(hotel_id)
        if hotel is None or hotel.date_removed is not None:
            abort(HTTPStatus.NOT_FOUND, description=HOTEL_NOT_FOUND)
        return hotel

    def create(self, data):
        hotel = Hotel(name=data["name"],
                      city=data["city"],
                      stars=data["stars"])

        return self.hotel_repository.save(hotel)

    def update(self, hotel_id, data):
        hotel: Hotel = self.get_or_404(hotel_id)

        hotel.name = data["name"]
        hotel.city = data["city"]
        hotel.stars = data["stars"]

        return self.hotel_repository.save(hotel)

    def delete(self, hotel_id):
        hotel: Hotel = self.get_or_404(hotel_id)
        hotel.date_removed = datetime.now(timezone.utc)
        self.hotel_repository.save(hotel)
