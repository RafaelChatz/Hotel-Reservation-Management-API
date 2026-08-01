from flask import Blueprint, request, abort
from marshmallow import ValidationError
from http import HTTPStatus

from ..messages import CUSTOMER_EMAIL_EXISTS, CUSTOMER_NOT_FOUND
from ..schemas.customer import customer_schema, customers_schema
from ..extensions import db
from ..models.customer import Customer

customers_bp = Blueprint('customers', __name__, url_prefix='/customers')


def get_customer_or_404(customer_id) -> Customer:
    customer: Customer = db.session.get(Customer, customer_id)
    if customer is None:
        abort(HTTPStatus.NOT_FOUND, description=CUSTOMER_NOT_FOUND)
    return customer


def validate_customer_email(email):
    existing_customer = db.session.query(Customer).filter_by(
        email=email
    ).first()

    if existing_customer:
        abort(HTTPStatus.CONFLICT, description=CUSTOMER_EMAIL_EXISTS)


@customers_bp.route("/", methods=["GET"])
def get_customers():
    customers_list: list[Customer] = db.session.query(Customer).all()
    return customers_schema.dump(customers_list)


@customers_bp.route("/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    customer: Customer = get_customer_or_404(customer_id)
    return customer_schema.dump(customer)


@customers_bp.route("/", methods=["POST"])
def create_customer():
    try:
        data = customer_schema.load(request.get_json())
    except ValidationError as err:
        abort(HTTPStatus.BAD_REQUEST, description=err.messages)

    validate_customer_email(data["email"])

    customer = Customer(first_name=data["first_name"], last_name=data["last_name"], email=data["email"])
    db.session.add(customer)
    db.session.commit()
    return customer_schema.dump(customer), HTTPStatus.CREATED
