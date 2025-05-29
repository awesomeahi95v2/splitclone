from flask import Blueprint, request, jsonify
from services.expense import ExpenseService

expense_bp = Blueprint("expense", __name__)

@expense_bp.route("/groups/<group_id>/expenses", methods=["POST"])
def add_expense(group_id):
    data = request.get_json()
    description = data.get("description")
    amount = data.get("amount")
    currency = data.get("currency", "GBP")
    paid_by = data.get("paid_by")
    created_by = data.get("created_by_user_id")
    involved_user_ids = data.get("involved_user_ids")

    if not all([description, amount, paid_by, created_by, involved_user_ids]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        expense = ExpenseService.add_expense(
            description,
            amount,
            currency,
            paid_by,
            created_by,
            group_id,
            involved_user_ids
        )
        return jsonify(expense.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@expense_bp.route("/expenses/<expense_id>", methods=["PUT"])
def edit_expense(expense_id):
    data = request.get_json()
    user_id = data.get("user_id")
    involved_user_ids = data.get("involved_user_ids")  # Optional, but now supported

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    try:
        expense = ExpenseService.edit_expense(
            expense_id,
            user_id,
            description=data.get("description"),
            amount=data.get("amount"),
            currency=data.get("currency"),
            paid_by=data.get("paid_by"),
            involved_user_ids=involved_user_ids
        )
        return jsonify(expense.to_dict()), 200
    except (ValueError, PermissionError) as e:
        return jsonify({"error": str(e)}), 403

@expense_bp.route("/expenses/<expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    try:
        ExpenseService.delete_expense(expense_id, user_id)
        return jsonify({"message": "Expense deleted"}), 200
    except (ValueError, PermissionError) as e:
        return jsonify({"error": str(e)}), 403

@expense_bp.route("/groups/<group_id>/expenses", methods=["GET"])
def list_expenses(group_id):
    expenses = ExpenseService.get_expenses_by_group(group_id)
    return jsonify([e.to_dict() for e in expenses]), 200
