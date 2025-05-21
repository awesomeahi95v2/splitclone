from flask import Blueprint, request, jsonify
from services.user import UserService

user_bp = Blueprint("user", __name__)

@user_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    try:
        user = UserService.create_user(email, password)
        return jsonify(user.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    user = UserService.authenticate(email, password)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify(user.to_dict()), 200