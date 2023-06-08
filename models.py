from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base


TableModel = declarative_base()


class UserModel(TableModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(40), unique=True, nullable=False, index=True)
    password = Column(String(256))


class FileModel(TableModel):
    __tablename__ = 'files'

    hash = Column(String(32), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))