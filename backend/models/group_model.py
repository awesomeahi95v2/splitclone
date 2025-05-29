import uuid
from db import db

class GroupModel(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(80), nullable=False)
    created_by = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)

    memberships = db.relationship('GroupMembership', backref='group', cascade='all, delete-orphan')
    expenses = db.relationship('ExpenseModel', backref='group', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_by": self.created_by,
            "members": [m.user_id for m in self.memberships if m.status == "joined"],
            "expenses": [expense.to_dict() for expense in self.expenses]
        }
