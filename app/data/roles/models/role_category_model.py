from sqlalchemy import Column, String, Integer, UUID, text
from sqlalchemy.orm import relationship

from setup import db


class RoleCategoryModel(db.Model):
    __tablename__ = 'role_category'
    id_role_category = Column(UUID, primary_key=True, unique=True, server_default=text('gen_random_uuid()'), nullable=False)
    name = Column(String(255), unique=True, nullable=False)
    color = Column(String(255), nullable=False)


    roles = relationship('RoleModel', back_populates='role_category', lazy=True)
    role_requests = relationship('RoleRequestModel', back_populates='role_category', lazy=True)
