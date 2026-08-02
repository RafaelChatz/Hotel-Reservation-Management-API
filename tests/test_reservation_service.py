import pytest

from http import HTTPStatus
from werkzeug.exceptions import HTTPException
from app.services.reservation import ReservationService
from app.models.hotel import Hotel
from app.models.customer import Customer
from app.models.reservation import Reservation, StatusType

def reservation_data():
    return {
        "hotel_id": 1,
        "customer_id": 2,
        "check_in": "2026-08-01",
        "check_out": "2026-08-03",
        "total_price": 100,
        "status": "ACTIVE",
    }

def test_create_reservation_when_hotel_does_not_exist_returns_not_found(mocker):
    service = ReservationService()

    # Arrange
    mocker.patch.object(
        service.hotel_service.hotel_repository,
        "get_by_id",
        return_value=None,
    )

    # Act
    with pytest.raises(HTTPException) as exc:
        service.create(reservation_data())

    # Assert
    assert exc.value.code == HTTPStatus.NOT_FOUND


def test_create_reservation_when_customer_does_not_exist_returns_not_found(mocker):
    service = ReservationService()

    # Arrange
    mocker.patch.object(
        service.hotel_service.hotel_repository,
        "get_by_id",
        return_value=Hotel(
            name="Test Hotel",
            city="Athens",
            stars=5,
        )
    )

    mocker.patch.object(
        service.customer_service.customer_repository,
        "get_by_id",
        return_value=None,
    )

    # Act
    with pytest.raises(HTTPException) as exc:
        service.create(reservation_data())

    # Assert
    assert exc.value.code == HTTPStatus.NOT_FOUND


def test_create_reservation_when_overlap_exists_returns_conflict(mocker):
    service = ReservationService()

    # Arrange
    mocker.patch.object(
        service.hotel_service.hotel_repository,
        "get_by_id",
        return_value=Hotel(
            name="Test Hotel",
            city="Athens",
            stars=5,
        ),
    )

    mocker.patch.object(
        service.customer_service.customer_repository,
        "get_by_id",
        return_value=Customer(
            first_name="Test",
            last_name="Name",
            email="test@mail.com",
        ),
    )

    mocker.patch.object(
        service.reservation_repository,
        "get_overlapping",
        return_value=Reservation(
            hotel_id=1,
            customer_id=2,
            check_in="2026-08-01",
            check_out="2026-08-03",
            total_price=451.00,
            status=StatusType.ACTIVE
        ),
    )

    # Act
    with pytest.raises(HTTPException) as exc:
        service.create(reservation_data())

    # Assert
    assert exc.value.code == HTTPStatus.CONFLICT


def test_create_reservation_when_request_is_valid_returns_reservation(mocker):
    service = ReservationService()

    # Arrange
    mocker.patch.object(
        service.hotel_service.hotel_repository,
        "get_by_id",
        return_value=Hotel(
            name="Test Hotel",
            city="Athens",
            stars=5,
        ),
    )

    mocker.patch.object(
        service.customer_service.customer_repository,
        "get_by_id",
        return_value=Customer(
            first_name="Test",
            last_name="Name",
            email="test@mail.com",
        ),
    )

    mocker.patch.object(
        service.reservation_repository,
        "get_overlapping",
        return_value=None,
    )

    reservation: Reservation = Reservation(
        hotel_id=1,
        customer_id=2,
        check_in="2026-08-01",
        check_out="2026-08-03",
        total_price=100,
        status=StatusType.ACTIVE
    )

    mocker.patch.object(
        service.reservation_repository,
        "save",
        return_value=reservation,
    )

    # Act
    result = service.create(reservation_data())

    # Assert
    assert result == reservation


def test_cancel_reservation_when_reservation_does_not_exist_returns_not_found(mocker):
    service = ReservationService()

    # Arrange
    mocker.patch.object(
        service.reservation_repository,
        "get_by_id",
        return_value=None,
    )

    reservation_id = 1

    # Act
    with pytest.raises(HTTPException) as exc:
        service.cancel(reservation_id)

    # Assert
    assert exc.value.code == HTTPStatus.NOT_FOUND


def test_cancel_reservation_when_reservation_exists_marks_it_cancelled(mocker):
    service = ReservationService()

    # Arrange
    reservation: Reservation = Reservation(
        hotel_id=1,
        customer_id=2,
        check_in="2026-08-01",
        check_out="2026-08-03",
        total_price=100,
        status=StatusType.ACTIVE
    )

    mocker.patch.object(
        service.reservation_repository,
        "get_by_id",
        return_value=reservation,
    )

    save_mock = mocker.patch.object(
        service.reservation_repository,
        "save",
        return_value=reservation,
    )

    reservation_id = 1

    # Act
    service.cancel(reservation_id)

    # Assert
    assert reservation.status == StatusType.CANCELLED
    save_mock.assert_called_once_with(reservation)


def test_cancel_all_with_hotel_id_calls_repository(mocker):
    service = ReservationService()

    # Arrange
    cancel_mock = mocker.patch.object(
        service.reservation_repository,
        "cancel_all_with_hotel_id",
    )

    hotel_id = 5

    # Act
    service.cancel_all_with_hotel_id(hotel_id)

    # Assert
    cancel_mock.assert_called_once_with(hotel_id)


def test_search_invalid_status_returns_bad_request():
    service = ReservationService()

    # Arrange
    filters = {
        "status": "INVALID"
    }

    # Act
    with pytest.raises(HTTPException) as exc:
        service.search(filters)

    # Assert
    assert exc.value.code == HTTPStatus.BAD_REQUEST


def test_search_when_filters_are_valid_returns_matching_reservations(mocker):
    service = ReservationService()

    # Arrange
    filters = {
        "status": "ACTIVE"
    }

    reservations = [
        Reservation(
            hotel_id=1,
            customer_id=2,
            check_in="2026-08-01",
            check_out="2026-08-03",
            total_price=100,
            status=StatusType.ACTIVE,
        )
    ]

    search_mock = mocker.patch.object(
        service.reservation_repository,
        "search",
        return_value=reservations,
    )

    # Act
    result = service.search(filters)

    # Assert
    search_mock.assert_called_once_with(filters)
    assert result == reservations
