from app import app
from db import db
from models import UserModel, GroupModel, ExpenseModel, GroupMembership

with app.app_context():
    GroupMembership.query.delete()
    ExpenseModel.query.delete()
    GroupModel.query.delete()
    UserModel.query.delete()
    db.session.commit()
