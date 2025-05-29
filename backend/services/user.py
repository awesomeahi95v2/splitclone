from models import UserModel
from backend.db import db

class UserService:
    @staticmethod
    def create_user(email, password):
        if UserModel.query.filter_by(email=email).first():
            raise ValueError("Email already in use.")

        user = UserModel(email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def authenticate(email, password):
        user = UserModel.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return user
        return None

    @staticmethod
    def get_user_by_id(user_id):
        return UserModel.query.get(user_id)
