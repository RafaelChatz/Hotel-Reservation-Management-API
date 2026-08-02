import pytest

from http import HTTPStatus
from werkzeug.exceptions import HTTPException
from datetime import datetime
from app.services.hotel import HotelService
from app.models.hotel import Hotel


def hotel_data():
    return {
        "name": "Test name",
        "city": "Test city",
        "stars": "4"
    }


def test_create_hotel_when_request_is_valid_returns_hotel(mocker):
    service = HotelService()

    hotel = Hotel(
        name="Test name",
        city="Test city",
        stars=4,
    )

    save_mock = mocker.patch.object(
        service.hotel_repository,
        "save",
        return_value=hotel
    )

    result = service.create(hotel_data())

    save_mock.assert_called_once()
    assert result == hotel


def test_update_hotel_when_hotel_exists_returns_updated_hotel(mocker):
    service = HotelService()

    hotel = Hotel(
        name="Test name",
        city="Test city",
        stars=4,
    )

    mocker.patch.object(
        service.hotel_repository,
        "get_by_id",
        return_value=hotel
    )

    save_mock = mocker.patch.object(
        service.hotel_repository,
        "save",
        return_value=hotel
    )

    result = service.update(5, hotel_data())

    save_mock.assert_called_once()
    assert result == hotel


def test_update_hotel_when_hotel_does_not_exist_returns_not_found(mocker):
    service = HotelService()

    # No Hotel
    mocker.patch.object(
        service.hotel_repository,
        "get_by_id",
        return_value=None
    )

    with pytest.raises(HTTPException) as exc:
        service.update(5, hotel_data())

    assert exc.value.code == HTTPStatus.NOT_FOUND


def test_delete_hotel_when_hotel_does_not_exist_returns_not_found(mocker):
    service = HotelService()

    # No Hotel
    mocker.patch.object(
        service.hotel_repository,
        "get_by_id",
        return_value=None
    )

    with pytest.raises(HTTPException) as exc:
        service.delete(5)

    assert exc.value.code == HTTPStatus.NOT_FOUND


def test_delete_hotel_when_hotel_exists_marks_it_deleted(mocker):
    service = HotelService()

    hotel = Hotel(
        name="Test name",
        city="Test city",
        stars=4,
    )

    mocker.patch.object(
        service,
        "get_or_404",
        return_value=hotel,
    )

    save_mock = mocker.patch.object(
        service.hotel_repository,
        "save",
    )

    service.delete(1)

    assert hotel.date_removed is not None
    assert isinstance(hotel.date_removed, datetime)

    save_mock.assert_called_once_with(hotel)
