import uuid
from backend.db import db
from sqlalchemy.orm import relationship

class ExpenseModel(db.Model):
    __tablename__ = 'expenses'

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    description = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default="GBP")

    paid_by = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    created_by_user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    group_id = db.Column(db.String, db.ForeignKey('groups.id'), nullable=False)

    splits = relationship("ExpenseSplit", backref="expense", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "amount": self.amount,
            "currency": self.currency,
            "paid_by": self.paid_by,
            "created_by_user_id": self.created_by_user_id,
            "group_id": self.group_id,
            "splits": [
                {
                    "user_id": split.user_id,
                    "amount": split.amount
                }
                for split in self.splits
            ]
        }
