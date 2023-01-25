from fastapi import Request
from core.Response import success
from aioredis import Redis


async def test_my_redis(req: Request):
    redis: Redis = req.app.state.cache

    await redis.set(name="today", value="2023.1.25")
    value = await redis.get("today")

    return success(msg="test_my_redis", data=[value])
