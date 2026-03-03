from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

test_bp = Blueprint("test", __name__)


@test_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()

    return jsonify({"message": "Access granted", "user_id": current_user})
