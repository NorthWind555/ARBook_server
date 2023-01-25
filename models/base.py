from tortoise import fields
from tortoise.models import Model

"""
表结构配置文件
这个文件里面的模型都会自动生成表，如果对应表不存在的话
"""


class TimesModel(Model):
    create_time = fields.DatetimeField(auto_now_add=True, description='创建时间')
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        abstract = True  # 抽象模型，用于继承
        table = None


class Role(TimesModel):
    role_name = fields.CharField(max_length=15, description="角色名称")
    user: fields.ManyToManyRelation["User"] = \
        fields.ManyToManyField("base.User", related_name="role", on_delete=fields.CASCADE)
    access: fields.ManyToManyRelation["Access"] = \
        fields.ManyToManyField("base.Access", related_name="role", on_delete=fields.CASCADE)
    role_status = fields.BooleanField(default=False, description="True:启用 False:禁用")
    role_desc = fields.CharField(null=True, max_length=255, description='角色描述')

    class Meta:
        table_description = "角色表"
        table = "role"


class Access(TimesModel):
    role: fields.ManyToManyRelation[Role]
    access_name = fields.CharField(max_length=15, description="权限名称")
    parent_id = fields.IntField(default=0, description='父id')
    scopes = fields.CharField(unique=True, max_length=255, description='权限范围标识')
    access_desc = fields.CharField(null=True, max_length=255, description='权限描述')
    menu_icon = fields.CharField(null=True, max_length=255, description='菜单图标')
    is_check = fields.BooleanField(default=False, description='是否验证权限 True为验证 False不验证')
    is_menu = fields.BooleanField(default=False, description='是否为菜单 True菜单 False不是菜单')

    class Meta:
        table_description = "权限表"
        table = "access"


class User(TimesModel):
    role: fields.ManyToManyRelation[Role]
    name = fields.CharField(null=True, max_length=24, description="姓名")
    nickname = fields.CharField(default='newAccount', max_length=64, description='用户名')
    password = fields.CharField(null=True, max_length=255, description='密码')
    phone = fields.CharField(null=True, max_length=11, description="手机号")
    school = fields.CharField(null=True, max_length=64, description="学校")
    college = fields.CharField(null=True, max_length=64, description="学院")
    clazz = fields.CharField(null=True, max_length=64, description="班级")
    status = fields.SmallIntField(default=1, description='状态 0:禁用，1:正常')
    avatar = fields.CharField(null=True, max_length=512, description='头像')
    sex = fields.SmallIntField(default=0, null=True, description='0未知 1男 2女')
    client_host = fields.CharField(null=True, max_length=19, description="访问IP")
    del_flag = fields.SmallIntField(default=0, description='删除标记 0正常')

    class Meta:
        table_description = "用户表"
        table = "user"
