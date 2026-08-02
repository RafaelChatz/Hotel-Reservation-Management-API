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
    """
    Get all customers.
    ---
    tags:
        - Customers
    responses:
        200:
            description: List of customers.
    """
    customers_list: list[Customer] = customer_service.get_all()
    return customers_schema.dump(customers_list)


@customers_bp.route("/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    """
    Get customer by customer id.
    ---
    tags:
        - Customers
    parameters:
        - in: path
          name: customer_id
          type: integer
          required: true
          description: Customer ID
    responses:
        200:
            description: List of customers.
        404:
            description: Hotel not customer.
    """
    customer: Customer = customer_service.get_or_404(customer_id)
    return customer_schema.dump(customer)


@customers_bp.route("/", methods=["POST"])
def create_customer():
    """
    Create customer.
    ---
    tags:
        - Customers
    consumes:
        - application/json
    parameters:
        - in: body
          name: body
          required: true
          schema:
            type: object
            required:
                - first_name
                - last_name
                - email
            properties:
                first_name:
                    type: string
                    example: Matthew
                last_name:
                    type: string
                    example: Johnson
                email:
                    type: string
                    example: matthew.johnson@example.com
    responses:
        201:
            description: Customer created.
        400:
            description: Bad request (wrong JSON input).
    """
    try:
        data = customer_schema.load(request.get_json())
    except ValidationError as err:
        abort(HTTPStatus.BAD_REQUEST, description=err.messages)

    customer = customer_service.create(data)
    return customer_schema.dump(customer), HTTPStatus.CREATED
