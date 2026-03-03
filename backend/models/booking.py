from extensions import db 
from datetime import datetime

class Booking(db.Model):
    __tablename__ = "bookings"

    booking_id = db.Column(db.Integer , primary_key=True)
    
    car_id = db.Column(db.Integer , db.ForeignKey("cars.car_id"),nullable = False)

    owner_id = db.Column(db.Integer , db.ForeignKey("users.user_id"),nullable = False)

    customer_id = db.Column(db.Integer, db.ForeignKey("users.user_id"),nullable= False)

    start_date = db.Column(db.Date , nullable = False)
    end_date = db.Column(db.Date , nullable = False)

    total_amount = db.Column(db.Numeric(10,2) , nullable = False)
    status = db.Column(db.String(20),default = "pending") #pending, confirmed , cancelled

    created_at = db.Column(db.DateTime , default = datetime.utcnow)
