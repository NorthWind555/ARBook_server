from fastapi import APIRouter, Request
from .Login import login

ApiRouter = APIRouter(prefix="/v1")


@ApiRouter.get("/")
async def home(req: Request):
    return "hello"


ApiRouter.post("/login", summary="登录接口")(login)
