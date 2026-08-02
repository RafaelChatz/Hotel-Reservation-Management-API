from http import HTTPStatus
from flask import abort

from ..models.customer import Customer
from ..messages import CUSTOMER_NOT_FOUND, CUSTOMER_EMAIL_EXISTS

from ..repositories.customer import CustomerRepository


class CustomerService:
    def __init__(self):
        self.customer_repository = CustomerRepository()

    def get_all(self):
        return self.customer_repository.get_all()

    def get_or_404(self, customer_id) -> Customer:
        customer: Customer = self.customer_repository.get_by_id(customer_id)
        if customer is None:
            abort(HTTPStatus.NOT_FOUND, description=CUSTOMER_NOT_FOUND)
        return customer

    def create(self, data):
        self.validate_customer_email(data["email"])

        customer = Customer(first_name=data["first_name"],
                            last_name=data["last_name"],
                            email=data["email"])

        return self.customer_repository.save(customer)

    def validate_customer_email(self, email):
        existing_customer = self.customer_repository.get_by_email(email)

        if existing_customer:
            abort(HTTPStatus.CONFLICT, description=CUSTOMER_EMAIL_EXISTS)
