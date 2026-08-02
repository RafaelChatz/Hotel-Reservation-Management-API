from ..extensions import db
from ..models.hotel import Hotel


class HotelRepository:

    def get_all(self):
        return db.session.query(Hotel).all()

    def get_by_id(self, hotel_id):
        return db.session.get(Hotel, hotel_id)

    def save(self, hotel: Hotel):
        db.session.add(hotel)
        db.session.commit()
        return hotel