from flask import Blueprint, request, abort
from marshmallow import ValidationError
from http import HTTPStatus

from ..services.customer import CustomerService
from ..schemas.customer import customer_schema, customers_schema
from ..models.customer import Customer

customers_bp = Blueprint('customers', __name__, url_prefix='/customers')

customer_service = CustomerService()


@customers_bp.route("/", methods=["GET"])
def get_customers():
    customers_list: list[Customer] = customer_service.get_all()
    return customers_schema.dump(customers_list)


@customers_bp.route("/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    customer: Customer = customer_service.get_or_404(customer_id)
    return customer_schema.dump(customer)


@customers_bp.route("/", methods=["POST"])
def create_customer():
    try:
        data = customer_schema.load(request.get_json())
    except ValidationError as err:
        abort(HTTPStatus.BAD_REQUEST, description=err.messages)

    customer = customer_service.create(data)
    return customer_schema.dump(customer), HTTPStatus.CREATED
