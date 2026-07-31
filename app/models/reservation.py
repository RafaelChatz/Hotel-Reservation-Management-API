from __future__ import annotations
from sqlalchemy.orm import Mapped, relationship
from enum import Enum

from ..extensions import db


class StatusType(Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"


class Reservation(db.Model):
    __tablename__ = "reservations"

    id = db.Column(db.BigInteger, db.Identity(), primary_key=True)

    hotel_id = db.Column(db.ForeignKey("hotels.id"),
                         nullable=False)

    customer_id = db.Column(db.ForeignKey("customers.id"),
                            nullable=False)

    check_in = db.Column(db.Date, nullable=False)
    check_out = db.Column(db.Date, nullable=False)

    total_price = db.Column(db.Numeric(10, 2), nullable=False)  # fixed precision type for monetary values

    status = db.Column(db.Enum(StatusType), nullable=False,
                       default=StatusType.ACTIVE)

    hotel: Mapped[Hotel] = relationship("Hotel", back_populates="reservations")
    customer: Mapped[Customer] = relationship("Customer", back_populates="reservations")

    __table_args__ = (
        # Constraint: check_out must be strictly after check_in
        db.CheckConstraint(
            'check_out > check_in',
            name='check_dates_order'
        ),
        # Constraint: the price must be a positive number
        db.CheckConstraint(
            "total_price >= 0",
            name="check_total_price_non_negative"
        ),
    )