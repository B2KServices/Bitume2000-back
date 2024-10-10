from sqlalchemy import Column, ForeignKey, UUID, UniqueConstraint

from setup import db


class UserRoleModel(db.Model):
    __tablename__ = 'user_roles'

    id_user = Column(UUID, ForeignKey('user.id_user', ondelete='CASCADE') ,primary_key=True, nullable=False)
    id_role = Column(UUID, ForeignKey('role.id_role', ondelete='CASCADE'), primary_key=True, nullable=False)

    __table_args__ = (UniqueConstraint('id_user', 'id_role', name='uq_user_role'),)