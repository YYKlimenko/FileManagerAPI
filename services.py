import hashlib
from os import path, mkdir, rename, remove
from typing import Annotated

from fastapi import Depends, UploadFile, HTTPException
from fastapi.security import HTTPBasicCredentials

from repositories import FileRepository, UserRepository
from settings import security, root


class FileService:
    def __init__(self, repository: FileRepository = Depends()):
        self.repository = repository

    @staticmethod
    async def _create_file(file_name: str) -> None:
        file_location = path.join(root, file_name[:2])
        if not path.exists(file_location):
            mkdir(file_location)
        rename(
            path.join(root, 'temp'),
            path.join(file_location, file_name)
        )

    @staticmethod
    async def _delete_file(file_name: str) -> None:
        remove(path.join(
            root, file_name[:2], file_name
        ))

    async def create(self, uploaded_file: UploadFile, user_id: int) -> str:
        hash_ = hashlib.md5()
        with uploaded_file.file as u_file:
            with open(path.join(root, 'temp'), 'wb') as temp_file:
                for chunk in iter(lambda: u_file.read(4096), b""):
                    hash_.update(chunk)
                    temp_file.write(chunk)
        hash_ = hash_.hexdigest()
        self.repository.create(hash_, user_id)
        await self._create_file(hash_)
        return hash_

    async def delete(self, hash_: str):
        self.repository.delete(hash_)
        await self._delete_file(hash_)

    async def get_file(self, hash_: str):
        return self.repository.get(hash_)

    async def get_link(self, hash_: str) -> str | None:
        file = self.repository.get(hash_)
        if file:
            link = path.join(root, hash_[:2], f'{hash_}')
            return link


async def authenticate(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
        repository: UserRepository = Depends(),
) -> int:
    user = repository.get_user_by_username(credentials.username)
    if user:
        return user.id
    raise HTTPException(status_code=403)
