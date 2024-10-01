from setup import db
from sqlalchemy import UUID, Column, String, text


class UserModel(db.Model):
    __tablename__ = 'user'

    id_user = Column(UUID, primary_key=True, unique=True, server_default=text('gen_random_uuid()'), nullable=False)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    mail = Column(String, nullable=False)
    label = Column(String, nullable=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
