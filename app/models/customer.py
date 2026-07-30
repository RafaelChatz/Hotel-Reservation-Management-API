from ..extensions import db


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.BigInteger, db.Identity(), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False)  # RFC 5321 standard
