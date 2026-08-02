from http import HTTPStatus
from flask import abort

from .customer import CustomerService
from .hotel import HotelService
from ..messages import CUSTOMER_HAS_OVERLAPPING_RESERVATION, RESERVATION_NOT_FOUND, \
    INVALID_RESERVATION_STATUS

from ..repositories.reservation import ReservationRepository
from ..models.reservation import Reservation, StatusType


class ReservationService:

    def __init__(self):
        self.reservation_repository = ReservationRepository()
        self.customer_service = CustomerService()
        self.hotel_service = HotelService()

    def get_all(self):
        return self.reservation_repository.get_all()

    def get_or_404(self, reservation_id) -> Reservation:
        reservation: Reservation = self.reservation_repository.get_by_id(reservation_id)
        if reservation is None:
            abort(HTTPStatus.NOT_FOUND, description=RESERVATION_NOT_FOUND)
        return reservation

    def validate_no_overlap(self, customer_id, check_in, check_out):
        if self.reservation_repository.get_overlapping(customer_id, check_in, check_out):
            abort(HTTPStatus.CONFLICT, description=CUSTOMER_HAS_OVERLAPPING_RESERVATION)

    def create(self, data):
        self.hotel_service.get_or_404(data["hotel_id"])
        self.customer_service.get_or_404(data["customer_id"])
        self.validate_no_overlap(data["customer_id"], data["check_in"], data["check_out"])

        reservation = Reservation(hotel_id=data["hotel_id"],
                                  customer_id=data["customer_id"],
                                  check_in=data["check_in"],
                                  check_out=data["check_out"],
                                  total_price=data["total_price"],
                                  status=data['status'])

        return self.reservation_repository.save(reservation)

    def cancel_all_with_hotel_id(self, hotel_id):
        self.reservation_repository.cancel_all_with_hotel_id(hotel_id)

    def cancel(self, reservation_id):
        reservation: Reservation = self.get_or_404(reservation_id)
        reservation.status = StatusType.CANCELLED  # idempotent no need to check if already canceled
        self.reservation_repository.save(reservation)

    def search(self, filters) -> list[Reservation]:
        if filters.get("status") and filters.get("status") not in StatusType.__members__:
            abort(HTTPStatus.BAD_REQUEST, description={
                "status": [
                    INVALID_RESERVATION_STATUS
                ]
            })

        return self.reservation_repository.search(filters)
