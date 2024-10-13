from sqlalchemy.orm import relationship
from setup import db
from sqlalchemy import UUID, Column, String, text, ForeignKey

user_role = db.Table(
    'user_role',
    Column('id_user', UUID, ForeignKey('user.id_user', ondelete='CASCADE'), primary_key=True),
    Column('id_role', UUID, ForeignKey('role.id_role', ondelete='CASCADE'), primary_key=True)
)

user_role_request = db.Table(
    'user_role_request',
    Column('id_user', UUID, ForeignKey('user.id_user', ondelete='CASCADE'), primary_key=True),
    Column('id_request_role', UUID, ForeignKey('role_request.id_request_role', ondelete='CASCADE'), primary_key=True)
)

class UserModel(db.Model):
    __tablename__ = 'user'

    id_user = Column(UUID, primary_key=True, unique=True, server_default=text('gen_random_uuid()'), nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=True)
    id_discord = Column(String, unique=True, nullable=False)
    avatar_url = Column(String, nullable=True)

    roles = relationship('RoleModel', secondary=user_role, back_populates='users')
    role_requests = relationship('RoleRequestModel', back_populates='requester', lazy=True)
    approved_role_requests = relationship('RoleRequestModel', secondary=user_role_request, back_populates='approved_users', lazy=True)