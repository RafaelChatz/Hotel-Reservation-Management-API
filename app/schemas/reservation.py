from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import validate, validates_schema, ValidationError

from ..messages import CHECK_OUT_AFTER_CHECK_IN
from ..models.reservation import Reservation, StatusType


class ReservationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Reservation
        include_fk = True

    total_price = auto_field(validate=validate.Range(min=0))

    status = auto_field(required=True,
                        validate=validate.OneOf(list(StatusType))
                        )

    @validates_schema
    def validate_dates(self, data, **kwargs):
        check_in = data.get("check_in")
        check_out = data.get("check_out")

        if check_in and check_out and check_in >= check_out:
            raise ValidationError(
                CHECK_OUT_AFTER_CHECK_IN,
                field_name="check_out"
            )


reservation_schema = ReservationSchema()
reservations_schema = ReservationSchema(many=True)
