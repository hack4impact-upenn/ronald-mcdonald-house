from .. import db
from sqlalchemy import Column, Integer, Boolean


class Guest(db.Model):
    _tablename_ = "guests"
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Guest Information
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    relationship_to_patient = db.Column(db.String(100))
    email = db.Column(db.String(200))
    guardian = db.Column(db.Boolean())
    dob = db.Column(db.Date)

    # Room Request
    room_request_id = db.Column(db.Integer, db.ForeignKey('room_requests.id'))

    def __repr__(self):
        return f'<Guest: {self.first_name} {self.last_name}>'

    def print_info(self):
        print('<Guest \n'
            f'First Name: {self.first_name}\n'
            f'Last Name: {self.last_name}\n'
            f'Relationship to Patient: {self.relationship_to_patient}\n'
            f'Email: {self.email}\n'
            f'Guardian: {self.guardian}\n'
            f'Guest DOB: {self.dob}\n')

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def generate_fake(room_request, **kwargs):
        """Generate fake guests for testing."""
        from sqlalchemy.exc import IntegrityError
        from faker import Faker
        from random import choice, randint, seed

        fake = Faker()
        seed()
        for i in range(randint(1, 5)):
            guest = Guest(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                relationship_to_patient=choice(["Mother", "Father", "Spouse"]),
                email=fake.email(),
                guardian=choice([True, False]),
                dob=fake.date_between(start_date="-30y", end_date="today"),
                room_request=room_request)
            db.session.add(guest)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()