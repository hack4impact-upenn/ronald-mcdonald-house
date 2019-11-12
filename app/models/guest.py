from .. import db
from sqlalchemy import Column, Integer, Boolean


class Guest(db.Model):
    _tablename_ = "guests"
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Guest Information
    name = db.Column(db.String(200))
    relationship_to_patient = db.Column(db.String(100))
    email = db.Column(db.String(200))
    guardian = db.Column(db.Boolean())
    dob = db.Column(db.Date)

    # Room Request
    room_request_id = db.Column(db.Integer, db.ForeignKey('room_requests.id'))

    def __repr__(self):
        return f'<Guest: {self.name}>'

    def print_info(self):
        print('<Guest \n'
            f'Name: {self.name}\n'
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
                name=fake.name(),
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