from extensions import db
from datetime import datetime

class Payment(db.Model):
    __tablename__="payments"

    payment_id =db.Column(db.Integer , primary_key= True , nullable = False)
    booking_id = db.Column(db.Integer ,db.ForeignKey("bookings.booking_id",),nullable=False)

    amount = db.Column(db.Numeric(10,2),nullable= False)
    
    payment_mode = db.Column(db.String(50) , default = "incomplete")
    #UPI , COD
    
    payment_status = db.Column(db.String(20),default ="pending") #pending , completed , failed

    payment_date = db.Column(db.DateTime, default = datetime.utcnow)

    #Relationship
    booking = db.relationship("Booking",backref = "payments")