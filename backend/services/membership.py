from models import UserModel
from models import GroupMembership
from db import db

class MembershipService:
    @staticmethod
    def invite_user_to_group_by_email(email, group_id, role='member'):
        user = UserModel.query.filter_by(email=email).first()
        if not user:
            raise ValueError("No user with that email exists.")

        existing = GroupMembership.query.filter_by(user_id=user.id, group_id=group_id).first()
        if existing:
            raise ValueError("User already invited or is a group member.")

        membership = GroupMembership(
            user_id=user.id,
            group_id=group_id,
            role=role,
            status='pending'
        )
        db.session.add(membership)
        db.session.commit()
        return membership
    
    @staticmethod
    def respond_to_invite(user_id, group_id, accept=True):
        membership = GroupMembership.query.filter_by(user_id=user_id, group_id=group_id).first()
        if not membership:
            raise ValueError("No invite found.")

        membership.status = 'joined' if accept else 'declined'
        db.session.commit()
        return membership

    @staticmethod
    def get_members_of_group(group_id):
        return GroupMembership.query.filter_by(group_id=group_id, status='joined').all()

