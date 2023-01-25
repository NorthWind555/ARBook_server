from typing import Callable
from fastapi import FastAPI
from database.mysql_cfg import register_mysql
from database.redis_cfg import get_redis


def startup(app: FastAPI) -> Callable:
    """
    FastApi 启动完成事件
    :param app: FastAPI
    :return: start_app
    """

    async def app_start() -> None:
        # APP启动完成后触发
        print("fastapi已启动")
        # 注册数据库
        await register_mysql(app)
        # 注入缓存到app state
        app.state.cache = await get_redis()
        print("redis初始化成功")
        pass

    return app_start


def stopping(app: FastAPI) -> Callable:
    """
    FastApi 停止事件
    :param app: FastAPI
    :return: stop_app
    """

    async def stop_app() -> None:
        # APP停止时触发
        print("fastapi已停止")

        pass

    return stop_app
