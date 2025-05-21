from models import ExpenseModel
from db import db

class ExpenseService:
    @staticmethod
    def add_expense(description, amount, currency, paid_by_user_id, created_by_user_id, group_id):
        expense = ExpenseModel(
            description=description,
            amount=amount,
            currency=currency,
            paid_by=paid_by_user_id,
            created_by_user_id=created_by_user_id,
            group_id=group_id
        )
        db.session.add(expense)
        db.session.commit()
        return expense

    @staticmethod
    def edit_expense(expense_id, user_id, **kwargs):
        expense = ExpenseModel.query.get(expense_id)
        if not expense:
            raise ValueError("Expense not found.")
        if expense.created_by_user_id != user_id:
            raise PermissionError("Only the creator can edit this expense.")

        editable_fields = {"description", "amount", "currency", "paid_by"}

        for field, value in kwargs.items():
            if field in editable_fields and hasattr(expense, field):
                setattr(expense, field, value)

        db.session.commit()
        return expense


    @staticmethod
    def delete_expense(expense_id, user_id):
        expense = ExpenseModel.query.get(expense_id)
        if not expense:
            raise ValueError("Expense not found.")
        if expense.created_by_user_id != user_id:
            raise PermissionError("Only the creator can delete this expense.")

        db.session.delete(expense)
        db.session.commit()
        return True

    @staticmethod
    def get_expenses_by_group(group_id):
        return ExpenseModel.query.filter_by(group_id=group_id).all()
    