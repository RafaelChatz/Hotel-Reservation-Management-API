from ..extensions import db
from ..models.customer import Customer


class CustomerRepository:

    def get_all(self):
        return db.session.query(Customer).all()

    def get_by_id(self, customer_id):
        return db.session.get(Customer, customer_id)

    def get_by_email(self, email):
        return db.session.query(Customer).filter_by(
            email=email
        ).first()

    def save(self, customer: Customer):
        db.session.add(customer)
        db.session.commit()
        return customer
