"""
认证模块
登录认证，权限认证等
"""

from datetime import timedelta, datetime
import jwt
from fastapi import HTTPException, Request
from fastapi.security import SecurityScopes
from fastapi.security.oauth2 import get_authorization_scheme_param
from jwt import PyJWTError
from pydantic import ValidationError
from starlette import status
from config import settings
from models.base import User, Access


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


async def check_permissions(req: Request, security_scopes: SecurityScopes):
    """
    权限验证
    :param req:
    :param security_scopes: 权限域
    :return:
    """
    # ----------------------------------------验证JWT token------------------------------------------------------------

    # 从请求头获取token
    authorization: str = req.headers.get("Authorization")
    scheme, token = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    print("token", token)
    print("scopes", security_scopes.scopes)
    user_id = await token_verify(token)
    # ---------------------------------------验证权限-------------------------------------------------------------------
    # 查询用户是否真实有效、或者已经被禁用
    check_user = await User().get_or_none(id=user_id)
    if not check_user or check_user.status != 1:
        raise get_unauthorized_exception(token, "用户不存在或已经被管理员禁用!")

    # # 用户权限验证
    # await user_permission_verify(req, security_scopes, user_id)

    # 缓存用户ID
    req.state.user_id = user_id


async def user_permission_verify(req: Request, security_scopes: SecurityScopes, user_id):
    """
    用户权限验证
    :param req:
    :param security_scopes:
    :param user_id:
    :return:
    """
    # 判断是否设置了权限域
    if security_scopes.scopes:
        # 返回当前权限域
        print("当前域：", security_scopes.scopes)
        # 用户权限域
        scopes = []

        is_pass = await Access.get_or_none(role__user__id=user_id, is_check=True,
                                           scopes__in=set(security_scopes.scopes),
                                           role__role_status=True)
        # 未查询到对应权限
        if not is_pass:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not permissions",
                headers={"scopes": security_scopes.scope_str},
            )
        # 查询用户所有权限
        scopes = await Access.filter(role__user__id=user_id, is_check=True,
                                     role__role_status=True).values_list("scopes")
        # 缓存用户全部权限
        req.state.scopes = scopes


async def token_verify(token):
    """
    token有效性验证并解析内容
    :param token:
    :return:
    """
    try:
        #
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        if payload:
            # 用户ID
            user_id = payload.get("user_id", None)
            # 用户手机号
            user_phone = payload.get("user_phone", None)
            # 无效用户信息
            if user_id is None or user_phone is None:
                raise get_unauthorized_exception(token, "无效凭证")

        else:
            raise get_unauthorized_exception(token, "无效凭证")

    except jwt.ExpiredSignatureError:

        raise get_unauthorized_exception(token, "凭证已过期")

    except jwt.InvalidTokenError:

        raise get_unauthorized_exception(token, "无效凭证")

    except (PyJWTError, ValidationError):

        raise get_unauthorized_exception(token, "无效凭证")
    return user_id


def get_unauthorized_exception(token, detail):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": f"Bearer {token}"},
    )
