from flask import Blueprint, request, jsonify
from extensions import db
from models.users import User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "renter")  # default to renter if not provided

    if role:
        role = role.strip().lower()

    # Optional
    if role not in ["owner", "renter"]:
        return jsonify({"message": "Invalid role"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    user = User(name=name, email=email, role=role)
    User.set_password(user, password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if user and User.check_password(user, password):
        access_token = create_access_token(identity=str(user.user_id))

        return (
            jsonify(
                {
                    "access_token": access_token,
                    "user_id": user.user_id,
                    "role": user.role,
                }
            ),
            200,
        )
    return jsonify({"message": "Invalid credentials"}), 401


@auth_bp.route("/asfd", methods=["GET"])
def getss():
    return jsonify({"message": "nioggas"}), 200
