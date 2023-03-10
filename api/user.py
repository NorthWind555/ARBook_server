from core.Response import success, fail
from validator.user import CreateUser, AccountLogin, UserInfo, AccountRegister
from models.base import User
from core.Utils import en_password, check_password
from core.Auth import create_access_token
from fastapi import Request
from fastapi.responses import JSONResponse


async def user_info(req: Request):
    """
    获取当前登陆用户信息
    :return:
    """
    user_data = await User.get_or_none(pk=req.state.user_id)
    if not user_data:
        return fail(msg=f"用户ID{req.state.user_id}不存在!")
    return success(msg="用户信息", data=UserInfo(**user_data.__dict__))


async def user_add(post: CreateUser):
    """
    创建用户
    :param post: CreateUser
    :return:
    """

    post.password = en_password(post.password)
    create_user = await User.create(**post.dict())
    if not create_user:
        return fail(msg=f"用户{post.phone}创建失败!")
    return success(msg=f"用户{create_user.phone}创建成功")


async def user_del(user_id: int):
    """
    删除用户
    :param user_id: int
    :return:
    """
    delete_user = await User.filter(pk=user_id).delete()
    if not delete_user:
        return fail(msg=f"用户{user_id}删除失败!")
    return success(msg="删除成功")


async def account_login(post: AccountLogin):
    """
    用户登陆
    :param post:
    :return: jwt token
    """
    get_user = await User.get_or_none(phone=post.phone)
    if not get_user:
        return fail(msg=f"用户{post.phone}密码验证失败!")
    if not check_password(post.password, get_user.password):
        return fail(msg=f"用户{post.phone}密码验证失败!")
    if not get_user.status:
        return fail(msg=f"用户{post.phone}已被管理员禁用!")
    jwt_data = {
        "user_id": get_user.pk,
        "user_phone": get_user.phone
    }
    jwt_token = create_access_token(data=jwt_data)
    return success(msg="登陆成功😄", data={"token": jwt_token})

    # # 直接注入到cookie里面
    # return JSONResponse({
    #     "code": 200,
    #     "message": "登陆成功😄",
    #     "data": {}
    # }, status_code=200, headers={"Set-Cookie": "X-token=Bearer " + jwt_token})


async def account_register(post: AccountRegister):
    # 验证激活码是否正确
    if post.active_code == "123":
        return await user_add(post)
    else:
        return fail(msg=f"激活码错误!")
