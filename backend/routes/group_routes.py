from flask import Blueprint, request, jsonify
from services.group import GroupService
from services.user import UserService
from services.membership import MembershipService

group_bp = Blueprint("group", __name__)

@group_bp.route("/groups/create", methods=["POST"])
def create_group():
    data = request.get_json()
    name = data.get("name")
    user_id = data.get("user_id")

    if not name or not user_id:
        return jsonify({"error": "Missing name or user ID"}), 400

    group = GroupService.create_group(name, created_by_user_id=user_id)
    return jsonify(group.to_dict()), 201

@group_bp.route("/groups/<group_id>", methods=["GET"])
def get_group(group_id):
    group = GroupService.get_group(group_id)
    if not group:
        return jsonify({"error": "Group not found"}), 404

    group_dict = group.to_dict()

    members = MembershipService.get_members_of_group(group_id)
    group_dict["members"] = [
        {"id": m.user.id, "email": m.user.email}
        for m in members
        if m.user is not None
    ]

    return jsonify(group_dict), 200

@group_bp.route("/groups/user/<user_id>", methods=["GET"])
def get_user_groups(user_id):
    user = UserService.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    groups = GroupService.get_groups_by_user(user)
    return jsonify([g.to_dict() for g in groups]), 200

@group_bp.route("/groups/<group_id>/invite", methods=["POST"])
def invite_user(group_id):
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    try:
        membership = MembershipService.invite_user_to_group_by_email(email, group_id)
        return jsonify(membership.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@group_bp.route("/groups/<group_id>/respond", methods=["POST"])
def respond_to_invite(group_id):
    data = request.get_json()
    user_id = data.get("user_id")
    accept = data.get("accept", True)

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    try:
        membership = MembershipService.respond_to_invite(user_id, group_id, accept=accept)
        return jsonify(membership.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
@group_bp.route("/groups/<group_id>/settle-up", methods=["GET"])
def settle_up(group_id):
    try:
        result = GroupService.settle_up(group_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400