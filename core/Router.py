"""
路由聚合
"""
import sys

# 如果此句报错，请忽略
from api.Base import ApiRouter
from fastapi import APIRouter

AllRouter = APIRouter()
# 如有需要，还可以include页面视图的router
AllRouter.include_router(ApiRouter)
