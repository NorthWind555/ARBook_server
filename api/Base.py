from fastapi import APIRouter, Request
from .Login import login
from .redisTest import test_my_redis

ApiRouter = APIRouter(prefix="/v1")


@ApiRouter.get("/")
async def home(req: Request):
    return "hello"


ApiRouter.post("/login", summary="登录接口")(login)
ApiRouter.post("/redis", summary="redis测试")(test_my_redis)
