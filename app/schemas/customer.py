from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import validate

from ..models.customer import Customer


class CustomerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Customer

    email = auto_field(validate=validate.Email())


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
