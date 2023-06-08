from typing import Type

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from settings import engine
from models import UserModel, FileModel


class UserRepository:
    model = UserModel

    def get_user_by_username(self, username: str) -> Type[model]:
        with Session(engine) as session:
            user = session.execute(
                select(self.model).where(self.model.username == username)
            ).scalar()
            return user if user else None


class FileRepository:
    model = FileModel

    def get(self, hash_: str) -> Type[model]:
        with Session(engine) as session:
            file = session.execute(
                select(self.model).where(self.model.hash == hash_)
            ).scalar()
            return file if file else None

    def create(self, hash_: str, user_id: int) -> None:
        try:
            with Session(engine) as session:
                session.add(self.model(hash=hash_, user_id=user_id))
                session.commit()
        except IntegrityError:
            return None

    def delete(self, hash_: str) -> None:
        with Session(engine) as session:
            session.execute(
                delete(self.model).where(self.model.hash == hash_)
            )
            session.commit()
