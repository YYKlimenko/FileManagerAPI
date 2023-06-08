from fastapi import FastAPI, Depends, UploadFile, HTTPException
from fastapi.responses import FileResponse

from models import TableModel
from services import authenticate, FileService
from settings import engine

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    TableModel.metadata.create_all(engine)


@app.post(
    '/',
    status_code=201,
    description='Upload a new file',
)
async def upload(
    file: UploadFile,
    service: FileService = Depends(),
    user_id: int = Depends(authenticate),
) -> str:
    return await service.create(file, user_id)


@app.delete(
    '/',
    status_code=200,
    description='Delete the file',
)
async def delete(
    hash_: str,
    service: FileService = Depends(),
    user_id: int = Depends(authenticate),
) -> None:
    if file := await service.get_file(hash_):
        if file.user_id != user_id:
            raise HTTPException(status_code=403)
        return await service.delete(hash_)


@app.get(
    '/',
    status_code=200,
    description='Download the file',
)
async def download(
    hash_: str,
    service: FileService = Depends(),
) -> FileResponse:
    if link := await service.get_link(hash_):
        return FileResponse(link)
