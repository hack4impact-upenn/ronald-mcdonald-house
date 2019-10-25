from .. import db
from sqlalchemy import Column, Integer, Boolean


class Guest(db.Model):
    _tablename_ = "guest"
    id = db.Column(db.Integer, primary_key=True)
    
    # Guest Information
    # Requester Personal Information
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    relationship_to_patient = db.Column(db.String(100))
    email = db.Column(db.String(1000))
    guardian = db.Column(db.Boolean())
    guest_dob = db.Column(db.Date)

    def __repr__(self):
        return f'<Guest: {self.first_name} {self.last_name}>'

    def print_info(self):
        print('<Guest \n'
            f'First Name: {self.first_name}\n'
            f'Last Name: {self.last_name}\n'
            f'Relationship to Patient: {self.relationship_to_patient}\n'
            f'Email: {self.email}\n'
            f'Guardian: {self.guardian}\n'
            f'Guest DOB: {self.guest_dob}\n')

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def generate_fake(count=10, **kwargs):
        """Generate a number of fake users for testing."""
        from sqlalchemy.exc import IntegrityError
        from random import seed, choice
        from faker import Faker

        fake = Faker()

        seed()
        for i in range(count):
            g = Guest(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                guardian=True)
            db.session.add(g)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()