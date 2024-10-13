from data.users.models.user_model import user_role
from setup import db
from sqlalchemy import UUID, Column, ForeignKey, String, text
from sqlalchemy.orm import relationship


class RoleModel(db.Model):
    __tablename__ = 'role'

    id_role = Column(UUID, primary_key=True, unique=True, server_default=text('gen_random_uuid()'), nullable=False)
    id_discord = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    id_role_category = Column(UUID, ForeignKey('role_category.id_role_category', ondelete='CASCADE'), nullable=False)

    role_category = relationship('RoleCategoryModel', back_populates='roles', lazy=True)
    users = relationship('UserModel', secondary=user_role, back_populates='roles')
