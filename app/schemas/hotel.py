from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import validate

from ..models.hotel import Hotel


class HotelSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Hotel
        exclude = ("date_removed",)
    stars = auto_field(
        validate=validate.Range(min=1, max=5),
    )

    date_removed = auto_field(dump_only=True)

hotel_schema = HotelSchema()
hotels_schema = HotelSchema(many=True)
