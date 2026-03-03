from flask import Blueprint, request, jsonify
from extensions import db
from models.cars import Cars
from models.users import User
from flask_jwt_extended import jwt_required, get_jwt_identity


car_bp = Blueprint("cars", __name__)


# CREATE CAR
@car_bp.route("/", methods=["POST"], strict_slashes=False)
@jwt_required()
def create_car():
    current_user_id = int(get_jwt_identity())    

    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    if user.role != "owner":
        return jsonify({"message": "only owners can add cars"}), 403

    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400
    
    required_fields = ["brand", "model", "price_per_day", "city"]
    missing_fields = []
    for field in required_fields:
        if not data.get(field):
            missing_fields.append(field)

    if missing_fields:
        return jsonify({"error": "Missing required fields", "missing": missing_fields}), 400
    

    car = Cars(
        brand=data.get("brand"),
        model=data.get("model"),
        price_per_day=data.get("price_per_day"),
        owner_id=current_user_id,
        city=data.get("city"),
        # availble at inital stage or should we ask user?
    )

    db.session.add(car)
    db.session.commit()

    return jsonify({"message": "car added successufully"}), 201


# GET ALL CARS
@car_bp.route("/", methods=["GET"], strict_slashes=False)
def get_cars():
    cars = Cars.query.all()

    result = []
    for car in cars:
        result.append(
            {
                "id": car.car_id,
                "brand": car.brand,
                "model": car.model,
                "price_per_day": car.price_per_day,
                "owner_id": car.owner_id,
                "is_available": car.is_available,
                "city": car.city,
            }
        )
    return jsonify(result), 200


# but we should query only the cars from the desired city of the customer


# GET SINGLE CAR
@car_bp.route("/<int:car_id>", methods=["GET"], strict_slashes=False)
def get_car(car_id):
    car = Cars.query.get(car_id)
    if not car:
        return jsonify({"message": "car not found"}), 404

    return (
        jsonify(
            {
                "id": car.car_id,
                "brand": car.brand,
                "model": car.model,
                "price_per_day": car.price_per_day,
                "owner_id": car.owner_id,
                "is_available": car.is_available,
                "city": car.city,
            }
        ),
        200,
    )


# UPDATE CAR
@car_bp.route("/<int:car_id>", methods=["PUT"], strict_slashes=False)
@jwt_required()
def update_car(car_id):
    
    current_user_id = int(get_jwt_identity())
    car = Cars.query.get(car_id)
    if not car:
        return jsonify({"message": "car not found"}), 404

    if car.owner_id != current_user_id:
        return jsonify({"message": "Not Authorized"}), 403

    data = request.get_json()

    car.brand = data.get("brand", car.brand)
    car.model = data.get("model", car.model)
    car.price_per_day = data.get("price_per_day", car.price_per_day)
    car.is_available = data.get("is_available", car.is_available)
    car.city = data.get("city", car.city)

    db.session.commit()

    return jsonify({"message": "car updated successfullu"}), 200


# DELETE CAR
@car_bp.route("/<int:car_id>", methods=["DELETE"], strict_slashes=False)
@jwt_required()
def delete_car(car_id):
    current_user_id = int(get_jwt_identity())
    car = Cars.query.get(car_id)
    if not car:
        return jsonify({"message": "car not found"}), 404

    if car.owner_id != current_user_id:
        return jsonify({"message": "Not authorized"}), 403

    db.session.delete(car)
    db.session.commit()

    return jsonify({"message": "car deleted successfully"}), 200
