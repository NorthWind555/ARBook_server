"""
认证模块
登录认证，权限认证等
"""

from datetime import timedelta, datetime
import jwt
from fastapi import HTTPException, Request, Depends
from fastapi.security import SecurityScopes
from fastapi.security.oauth2 import get_authorization_scheme_param, OAuth2PasswordBearer
from jwt import PyJWTError
from pydantic import ValidationError
from starlette import status
from config import settings
from models.base import User, Access

OAuth2 = OAuth2PasswordBearer("")


def create_access_token(data: dict):
    """
    创建token
    :param data: 加密数据
    :return: jwt
    """
    token_data = data.copy()
    # token超时时间
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    # 向jwt加入超时时间
    token_data.update({"exp": expire})
    # jwt加密
    jwt_token = jwt.encode(token_data, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    return jwt_token
