from sqlalchemy import Column, Integer, String, ForeignKey, UUID, text
from sqlalchemy.orm import relationship

from setup import db


class RoleRequestModel(db.Model):
    __tablename__ = 'role_request'

    id_request_role = Column(UUID, primary_key=True, unique=True, server_default=text('gen_random_uuid()'), nullable=False)
    approves = Column(Integer, server_default=text('0'), nullable=False)
    name = Column(String, nullable=False)
    id_user = Column(UUID, ForeignKey('user.id_user', ondelete='CASCADE'), nullable=False)
    id_role_category = Column(UUID, ForeignKey('role_category.id_role_category', ondelete='CASCADE'), nullable=False)

