from pydantic import BaseModel


class LoginModel(BaseModel):
    phone: str
    password: str


def login(data: LoginModel):
    return data
