from setup import db
from sqlalchemy import UUID, Column, String, text


class UserModel(db.Model):
    __tablename__ = 'user'

    id_user = Column(UUID, primary_key=True, unique=True, server_default=text('gen_random_uuid()'), nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    id_discord = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
