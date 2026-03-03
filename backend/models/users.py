from extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # owner or renter
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    cars = db.relationship("Car", backref="owner", lazy=True, cascade="all, delete")
    bookings = db.relationship("Booking", backref="user", lazy=True, cascade="all, delete")