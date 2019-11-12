from .. import db
from sqlalchemy import Column, Integer, Boolean, DateTime
from datetime import datetime
from .user import User


class Activity(db.Model):
    _tablename_ = "activity"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    text = db.Column(db.String())
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    room_request_id = db.Column(db.Integer, db.ForeignKey('room_requests.id'))

    def __repr__(self):
        return self.text

    def __str__(self):
        return self.__repr__()

    def print_info(self):
        print('<Activity: \n'
              f'created_at: {self.created_at}'
              f'text: {text}'
              f'user_id: {self.user_id}'
              f'user_name: {self.user.first_name} {self.user.last_name}'
              f'room_request_id: {self.room_request_id}')
    
    def generate_fake(room_request, **kwargs):
        """Generates fake activity for the given room request for testing."""
        from sqlalchemy.exc import IntegrityError
        from faker import Faker
        import random

        fake = Faker()
        random.seed()
        users = User.query.all()
        for i in range(random.randint(1, 10)):
            user = random.choice(users)
            activity = Activity(
                text=fake.paragraph(),
                user_id=user.id,
                room_request_id=room_request.id)
            db.session.add(activity)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
