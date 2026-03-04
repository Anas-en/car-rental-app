from flask import Blueprint, request, jsonify
from extensions import db
from models.cars import Cars
from models.users import User
from models.payments import Payment
from models.booking import Booking
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

booking_bp = Blueprint("bookings", __name__)



# Booking logic
@booking_bp.route("/", methods=["POST"])
@jwt_required()
def create_booking():

    current_user_id = int(get_jwt_identity())

    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    car_id = data.get("car_id")
    start_date_str = data.get("start_date")
    end_date_str = data.get("end_date")

    if not car_id or not start_date_str or not end_date_str:
        return jsonify({"error": "car_id , start_Date and end_Date required"}), 400

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Date Format must be YYYY-MM-DD"}), 400

    if start_date >= end_date:
        return jsonify({"error": "end_date must be after start_date"}), 400
    if start_date < datetime.utcnow().date():
        return jsonify({"error": "cannot book past date"}), 400

    # car = db.session.get(Cars, car_id)
    #lock car
    car = (
        db.session.query(Cars)
        .filter(Cars.car_id == car_id)
        .with_for_update()
        .first()
    )

    if not car:
        return jsonify({"error": "Car not found"}), 404

    if car.owner_id == current_user_id:
        return jsonify({"error": "You cannot book your own car"}), 400

    if not car.is_available:
        return jsonify({"error": "Car currently unavailable"}), 400

    
    # Booking date conflict
    
    conflict = Booking.query.filter(
        Booking.car_id == car_id,
        Booking.start_date <= end_date,
        Booking.end_date >= start_date,
        Booking.status.in_(["pending", "confirmed"]), # now if only do confirmed more request can be there
         
    ).first()

    if conflict:
        return jsonify({"error": "Car already booked for these dates"}), 400
    
    existing_request = Booking.query.filter(
        Booking.car_id == car_id,
        Booking.customer_id == current_user_id,
        Booking.start_date == start_date,
        Booking.end_date == end_date,
        Booking.status == "pending"
    ).first()
    
    if existing_request:
        return jsonify({"error": "You already requested this booking"}), 400


    days = (end_date - start_date).days
    total_amount = days * car.price_per_day

    booking = Booking(
        car_id=car_id,
        owner_id=car.owner_id,
        customer_id=current_user_id,
        start_date=start_date,
        end_date=end_date,
        total_amount=total_amount,
        status="pending",
        # "booking will remain in pending untill car_owner confirmed it"
    )


    try:
        db.session.add(booking)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error":"Database error",
            "details":str(e)
            }),500

    return (
        jsonify(
            {
                "message": "booking created successfully",
                "booking_id": booking.booking_id,
                "total_amount": float(total_amount),
            }
        ),
        201,
    )




# user can see bookings (Customer)
@booking_bp.route("/my", methods=["GET"])
@jwt_required()
def get_my_bookings():

    current_user_id = int(get_jwt_identity())

    bookings = Booking.query.filter_by(customer_id=current_user_id).all()

    result = []

    for b in bookings:
        result.append(
            {
                "booking_id": b.booking_id,
                "car_id": b.car_id,
                "start_date": b.start_date.isoformat(),
                "end_date": b.end_date.isoformat(),
                "car_brand": b.car.brand,
                "car_model": b.car.model,
                "car_owner_name": b.car.owner.name,
                "total_amount": float(b.total_amount),
                "status": b.status,
            }
        )

    return jsonify(result), 200



# GET bookings for my cars(owner)
@booking_bp.route("/owner", methods=["GET"])
@jwt_required()
def owner_bookings():

    current_user_id = int(get_jwt_identity())

    bookings = Booking.query.filter_by(owner_id=current_user_id).all()

    result = []

    for b in bookings:
        result.append(
            {
                "booking_id": b.booking_id,
                "car_id": b.car_id,
                "start_date": b.start_date.isoformat(),
                "end_date": b.end_date.isoformat(),
                "car_brand": b.car.brand,
                "car_model": b.car.model,
                "Renter_name": b.customer.name,
                "total_amount": float(b.total_amount),
                "status": b.status,
            }
        )
    return jsonify(result),200



#confirmation by owner
@booking_bp.route("/<int:booking_id>/confirm",methods=["PATCH"])
@jwt_required()
def confirm_booking(booking_id):
    current_user_id = int(get_jwt_identity())
    
    booking = db.session.get(Booking , booking_id)
    
    if not booking:
        return jsonify({"error":"Booking not found"}),404
    
    if booking.owner_id != current_user_id:
        return jsonify({"error":"only owner can confirm"}),403
    

    conflict = Booking.query.filter(
        Booking.car_id == booking.car_id,
        Booking.booking_id != booking.booking_id, 
        Booking.start_date <= booking.end_date,
        Booking.end_date >= booking.start_date,
        Booking.status == "confirmed"
    ).first()
    
    if conflict:
        return jsonify({"error":"Car already booked in this period"}),400
    
    if booking.status !="pending":
        return jsonify({"error":"only pending bookings can be confirmed"}),400
    
    booking.status = "confirmed"
    booking.car.is_available = False
    
    db.session.commit()
    
    return jsonify({"message":"Booking Confirmed"}),200


    
#owner rejects 
@booking_bp.route("/<int:booking_id>/reject",methods=["PATCH"])
@jwt_required()
def reject_booking(booking_id):
    
    current_user_id = int(get_jwt_identity())
    
    booking = db.session.get(Booking, booking_id)

    if not booking:
        return jsonify({"error":"Booking not found"}),404
    if booking.owner_id != current_user_id:
        return jsonify({"error":"only owner can reject"}),403
    
    if booking.status !="pending":
        return jsonify({"error":"Only pending bookings can be rejected"}),400
    
    booking.status = "cancelled"
    booking.car.is_available = True
    
    db.session.commit()
    
    return jsonify({"message":"Booking rejected"}),200



#Owner dashboard
@booking_bp.route("/owner/pending",methods = ["GET"])
@jwt_required()
def owner_pending_bookings():
    
    current_user_id = int(get_jwt_identity())
    
    bookings = Booking.query.filter_by(
        owner_id = current_user_id , 
        status = "pending"
    ).all()

    result = []
    
    for b in bookings:
        result.append({
            "booking_id":b.booking_id,
            "car_id":b.car_id,
            "customer_name": b.customer.name,
            "start_date":b.start_date.isoformat(),
            "end_date":b.end_date.isoformat(),
            "total_amount":float(b.total_amount),
            "status":b.status
        })
    
    return jsonify(result),200



#booking cancelled by customer
@booking_bp.route("/<int:booking_id>/cancel",methods=["PATCH"],strict_slashes=False)
@jwt_required()
def cancel_booking(booking_id):
    current_user_id = int(get_jwt_identity())
    
    booking = db.session.get(Booking , booking_id)
    
    
    if not booking:
        return jsonify({"error":"Booking not found"}),404
    if booking.customer_id != current_user_id:
        return jsonify({"error":"Not authorized"}),403
    
    if booking.status == "cancelled":
        return jsonify({"error": "Booking already cancelled"}), 400
    
    booking.status = "cancelled"
    
    booking.car.is_available = True
    
    db.session.commit()
    
    return jsonify(({"message":"Booking Cancelled"})),200