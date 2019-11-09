from .. import db
from sqlalchemy import Column, Integer, Boolean, DateTime
from .user import User
from .room_request import *
from datetime import datetime


class  Activity(db.Model):
    _tablename_ = "activty"

    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(DateTime, default= datetime.utcnow)    
    text = db.Column(db.String())
    commenter = db.Column(db.String())
    #forgin keys for user and 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    room_request_id = db.Column(db.Integer, db.ForeignKey('room_requests.id'))
    
    users = db.relationship('User', backref= ('activty'))
    room = db.relationship('RoomRequest', backref='activty')


    def __repr__(self):
        return self.text

    def print_info(self):
        print(f'<Last Activty was at: {self.created_at}. {self.text}>')

    def __str__(self):
        return self.__repr__()
    