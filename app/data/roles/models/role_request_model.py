from data.users.models.user_model import user_role_request
from setup import db
from sqlalchemy import UUID, Column, ForeignKey, String, text
from sqlalchemy.orm import relationship


class RoleRequestModel(db.Model):
    __tablename__ = 'role_request'

    id_request_role = Column(UUID, primary_key=True, unique=True, server_default=text('gen_random_uuid()'), nullable=False)
    name = Column(String, nullable=False)
    id_requester = Column(UUID, ForeignKey('user.id_user', ondelete='CASCADE'), nullable=False)
    id_role_category = Column(UUID, ForeignKey('role_category.id_role_category', ondelete='CASCADE'), nullable=False)

    approved_users = relationship('UserModel', secondary=user_role_request, back_populates='approved_role_requests', lazy=True)
    requester = relationship('UserModel', back_populates='role_requests')
    role_category = relationship('RoleCategoryModel', back_populates='role_requests')
