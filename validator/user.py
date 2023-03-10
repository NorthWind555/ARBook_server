"""
@Des: 用户验证模型
"""
from pydantic import Field, BaseModel
from typing import Optional


class CreateUser(BaseModel):
    """
    创建用户
    """
    phone: str
    password: str = Field(min_length=3, max_length=12)


class AccountRegister(CreateUser):
    """
    用户注册，需要验证码
    """
    active_code: str = Field(min_length=3, max_length=16)


class AccountLogin(BaseModel):
    phone: str
    password: str = Field(min_length=3, max_length=12)


class UserInfo(BaseModel):
    id: int
    name: str
    nickname: Optional[str]
    phone: str
    password: str
    user_status: bool
    sex: Optional[str]
    school: Optional[str]
    college: Optional[str]
    clazz: Optional[str]
    avatar: Optional[str]
