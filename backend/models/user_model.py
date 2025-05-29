import uuid
from db import db
from werkzeug.security import generate_password_hash, check_password_hash

class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    type = db.Column(db.String(50))

    memberships = db.relationship('GroupMembership', backref='user', cascade='all, delete-orphan')
    paid_expenses = db.relationship('ExpenseModel', foreign_keys='ExpenseModel.paid_by', backref='payer', cascade='all, delete-orphan')
    created_expenses = db.relationship('ExpenseModel', foreign_keys='ExpenseModel.created_by_user_id', backref='creator', cascade='all, delete-orphan')
    
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "groups": [m.group_id for m in self.memberships if m.status == "joined"]
        }