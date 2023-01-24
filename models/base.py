from tortoise import Model, fields


class User(Model):
    name = fields.CharField(null=True, max_length=24, description="姓名")
    nickname = fields.CharField(default='newAccount', max_length=64, description='用户名')
    password = fields.CharField(null=True, max_length=64, description='密码')
    phone = fields.CharField(null=True, max_length=11, description="手机号")
    school = fields.CharField(null=True, max_length=64, description="学校")
    college = fields.CharField(null=True, max_length=64, description="学院")
    clazz = fields.CharField(null=True, max_length=64, description="班级")
    status = fields.SmallIntField(default=0, description='状态 0:正常，1:禁用')
    avatar = fields.CharField(null=True, max_length=512, description='头像')
    sex = fields.SmallIntField(default=0, null=True, description='0未知 1男 2女')
    client_host = fields.CharField(null=True, max_length=19, description="访问IP")
    create_time = fields.DatetimeField(auto_now_add=True, description='创建时间')
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")
    del_flag = fields.SmallIntField(default=0, description='删除标记 0正常')

    class Meta:
        table_description = "用户"
        table = "user"
