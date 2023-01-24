from models.base import User
from pydantic import BaseModel


class LoginModel(BaseModel):
    phone: str
    password: str


async def login(data: LoginModel):
    u1 = await User().create(phone=data.phone, password=data.password)
    users = await User().all()
    if u1 is None:
        return {"user列表": users, "添加状态": "失败"}
    return {"user列表": users, "添加状态": "成功"}
