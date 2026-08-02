import pytest

from http import HTTPStatus
from werkzeug.exceptions import HTTPException
from app.services.customer import CustomerService
from app.models.customer import Customer


def customer_data():
    return {
        "first_name": "Test name",
        "last_name": "Test surname",
        "email": "test@test.com"
    }


def test_create_customer_when_email_does_not_exist_returns_customer(mocker):
    service = CustomerService()

    # Arrange
    customer = Customer(
        first_name="Test",
        last_name="Surname",
        email="test@test.com",
    )

    mocker.patch.object(
        service.customer_repository,
        "get_by_email",
        return_value=None,
    )

    save_mock = mocker.patch.object(
        service.customer_repository,
        "save",
        return_value=customer,
    )

    # Act
    result = service.create(customer_data())

    # Assert
    save_mock.assert_called_once()
    assert result == customer


def test_create_customer_when_email_already_exists_returns_conflict(mocker):
    service = CustomerService()

    # Arrange
    customer = Customer(
        first_name="Test",
        last_name="Surname",
        email="test@test.com",
    )

    mocker.patch.object(
        service.customer_repository,
        "get_by_email",
        return_value=customer,
    )

    # Act
    with pytest.raises(HTTPException) as exc:
        service.create(customer_data())

    # Assert
    assert exc.value.code == HTTPStatus.CONFLICT
