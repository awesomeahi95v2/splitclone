from backend.app import app
from backend.db import db
from models import UserModel, GroupModel, ExpenseModel, GroupMembership, ExpenseSplit

with app.app_context():
    ExpenseSplit.query.delete()
    GroupMembership.query.delete()
    ExpenseModel.query.delete()
    GroupModel.query.delete()
    UserModel.query.delete()
    db.session.commit()
