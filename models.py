from flask_sqlalchemy import SQLAlchemy # type: ignore
from datetime import datetime

db = SQLAlchemy()

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    package = db.Column(db.String(50), nullable=False)
    travel_date = db.Column(db.Date, nullable=False)
    num_travelers = db.Column(db.Integer, nullable=False)
    accommodation = db.Column(db.String(20), nullable=False)
    special_requirements = db.Column(db.Text)
    contact_person = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')

    def to_dict(self):
        return {
            'id': self.id,
            'package': self.package,
            'travel_date': self.travel_date.strftime('%Y-%m-%d'),
            'num_travelers': self.num_travelers,
            'accommodation': self.accommodation,
            'special_requirements': self.special_requirements,
            'contact_person': self.contact_person,
            'mobile': self.mobile,
            'email': self.email,
            'booking_date': self.booking_date.strftime('%Y-%m-%d %H:%M:%S'),
            'status': self.status
        }