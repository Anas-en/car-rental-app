from extensions import db
from datetime import datetime


class Cars(db.Model):
    __tablename__ = "cars"

    car_id = db.Column(
        db.Integer,
        primary_key=True,
    )
    owner_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    price_per_day = db.Column(db.Numeric(10, 2), nullable=False)

    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    bookings = db.relationship(
        "Booking", backref="car", lazy=True, cascade="all, delete"
    )