from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import validate

from ..models.hotel import Hotel


class HotelSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Hotel

    stars = auto_field(
        validate=validate.Range(min=1, max=5),
    )


hotel_schema = HotelSchema()
hotels_schema = HotelSchema(many=True)
