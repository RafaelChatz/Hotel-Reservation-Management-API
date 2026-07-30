from ..extensions import db


class Hotel(db.Model):
    __tablename__ = "hotels"

    id = db.Column(db.BigInteger, db.Identity(), primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    stars = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        # Constraint: stars must be between 1 and 5
        db.CheckConstraint(
            "stars >= 1 AND stars <= 5",
            name="check_hotel_stars_range"
        ),
    )
