from sqlalchemy import Column, Integer, String, ForeignKey, UUID
from sqlalchemy.orm import relationship

from setup import db


class RoleModel(db.Model):
    __tablename__ = 'role'

    id_role = Column(UUID, primary_key=True, unique=True, nullable=False)
    id_discord = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    id_role_category = Column(UUID, ForeignKey('role_category.id_role_category'), nullable=False)

    role_category = relationship('RoleCategoryModel', back_populates='roles', lazy=True)