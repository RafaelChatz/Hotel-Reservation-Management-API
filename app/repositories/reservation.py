from datetime import datetime

from ..models.customer import Customer
from ..models.hotel import Hotel
from ..models.reservation import Reservation, StatusType
from ..extensions import db


class ReservationRepository:

    def get_all(self):
        return db.session.query(Reservation).all()

    def get_by_id(self, reservation_id) -> Reservation:
        return db.session.get(Reservation, reservation_id)

    def get_overlapping(self, customer_id, check_in, check_out):
        return (
            db.session.query(Reservation)
            .filter(
                Reservation.customer_id == customer_id,
                Reservation.status == StatusType.ACTIVE,
                Reservation.check_in <= check_out,
                Reservation.check_out >= check_in,
            )
            .first()
        )

    def save(self, reservation: Reservation):
        db.session.add(reservation)
        db.session.commit()
        return reservation

    def search(self, filters):
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

    def cancel_all_with_hotel_id(self, hotel_id):
        reservations: list[Reservation] = db.session.query(Reservation).filter(
            Reservation.hotel_id == hotel_id
        ).all()

        for reservation in reservations:
            reservation.status = StatusType.CANCELLED

        db.session.commit()