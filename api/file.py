from fastapi import APIRouter
from fastapi.responses import FileResponse

from core.Response import fail
from models.base import File

router = APIRouter(prefix='/file')


@router.get("/download")
async def download(name: str):
    file = await File.get_or_none(name=name)
    if not file:
        return fail(msg="文件不存在")
    return FileResponse(file.url, filename=file.name)
