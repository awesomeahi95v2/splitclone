import uuid
from backend.db import db

class GroupMembership(db.Model):
    __tablename__ = 'group_memberships'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    group_id = db.Column(db.String, db.ForeignKey('groups.id'), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.String, default='member')  # e.g., 'member', 'admin'
    status = db.Column(db.String, default='pending')  # 'pending', 'joined', 'declined'

    def to_dict(self):
        return {
            "id": self.id,
            "group_id": self.group_id,
            "user_id": self.user_id,
            "role": self.role,
            "status": self.status
        }
