from models import ExpenseModel, ExpenseSplit
from db import db

class ExpenseService:
    @staticmethod
    def add_expense(description, amount, currency, paid_by_user_id, created_by_user_id, group_id, involved_user_ids):
        if not involved_user_ids:
            raise ValueError("At least one member must be involved in the expense.")

        split_amount = round(amount / len(involved_user_ids), 2)
        expense = ExpenseModel(
            description=description,
            amount=amount,
            currency=currency,
            paid_by=paid_by_user_id,
            created_by_user_id=created_by_user_id,
            group_id=group_id
        )
        db.session.add(expense)
        db.session.flush()  # get expense.id before commit

        for user_id in involved_user_ids:
            split = ExpenseSplit(
                expense_id=expense.id,
                user_id=user_id,
                amount=split_amount
            )
            db.session.add(split)

        db.session.commit()
        return expense

    @staticmethod
    def edit_expense(expense_id, user_id, description=None, amount=None, currency=None, paid_by=None, involved_user_ids=None):
        expense = ExpenseModel.query.get(expense_id)
        if not expense:
            raise ValueError("Expense not found.")
        if expense.created_by_user_id != user_id:
            raise PermissionError("Only the creator can edit this expense.")

        if description is not None:
            expense.description = description
        if amount is not None:
            expense.amount = amount
        if currency is not None:
            expense.currency = currency
        if paid_by is not None:
            expense.paid_by = paid_by

        if involved_user_ids is not None:
            # delete old splits
            for split in expense.splits:
                db.session.delete(split)

            split_amount = round(expense.amount / len(involved_user_ids), 2)
            for user_id in involved_user_ids:
                split = ExpenseSplit(
                    expense_id=expense.id,
                    user_id=user_id,
                    amount=split_amount
                )
                db.session.add(split)

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
