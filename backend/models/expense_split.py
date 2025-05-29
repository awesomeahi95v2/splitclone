import uuid
from db import db

class ExpenseSplit(db.Model):
    __tablename__ = 'expense_splits'

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    expense_id = db.Column(db.String, db.ForeignKey('expenses.id'), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
