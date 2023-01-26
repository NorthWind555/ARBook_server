from fastapi import APIRouter, Security
# from core.Auth import check_permissions
from api.user import user_info, user_add, user_del, account_login, account_register
from core.Auth import check_permissions

ApiRouter = APIRouter(prefix="/v1")


ApiRouter.post("/user/account/login", tags=["用户接口"], summary="用户登陆")(account_login)
ApiRouter.post("/user/account/register",
               tags=["用户接口"],
               summary="用户注册",
               )(account_register)


ApiRouter.get("/admin/user/info",
              tags=["用户管理"],
              summary="获取当前用户信息",
              dependencies=[Security(check_permissions)]
              )(user_info)

ApiRouter.delete("/admin/user/del",
                 tags=["用户管理"],
                 summary="用户删除",
                 dependencies=[Security(check_permissions, scopes=["user_delete"])]
                 )(user_del)

