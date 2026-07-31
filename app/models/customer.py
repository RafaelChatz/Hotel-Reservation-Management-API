from __future__ import annotations
from sqlalchemy.orm import Mapped, relationship
from typing import List

from ..extensions import db


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.BigInteger, db.Identity(), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False)  # RFC 5321 standard

    reservations: Mapped[List[Reservation]] = relationship("Reservation", back_populates="customer")

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
        }