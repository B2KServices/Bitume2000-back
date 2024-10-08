from sqlalchemy import Column, ForeignKey, UUID

from setup import db


class UserRoleModel(db.Model):
    __tablename__ = 'user_roles'

    id_user = Column(UUID, ForeignKey('user.id_user') ,primary_key=True, nullable=False)
    id_role = Column(UUID, ForeignKey('role.id_role'), primary_key=True, nullable=False)