# -*- coding: utf-8 -*-
# @Time : 2021/8/2 14:50
# @Author : 谢泽辉
# @Software : PyCharm

import pymysql
from timeit import default_timer
from DBUtils.PooledDB import PooledDB

#连接池的配置内容
class DMysqlConfig:
    """
        :param setsession:optional list of SQL commands that may serve to prepare
            the session, e.g. ["set datestyle to ...", "set time zone ..."]
        :param reset:how connections should be reset when returned to the pool
            (False or None to rollback transcations started with begin(),
            True to always issue a rollback for safety's sake)
    """
    def __init__(self, host, db, user, password, port=3306):
        self.host = host        #host:数据库ip地址
        self.port = port        #port:数据库端口
        self.db = db        #db:库名
        self.user = user
        self.password = password

        self.charset = 'UTF8'  # 不能是 utf-8  charset:字符编码
        self.minCached = 10     #mincached:连接池中空闲连接的初始数量
        self.maxCached = 20     #maxcached:连接池中空闲连接的最大数量
        self.maxShared = 10     #maxshared:共享连接的最大数量
        self.maxConnection = 100        #maxconnections:创建连接池的最大数量

        self.blocking = True    #blocking:超过最大连接数量时候的表现，为True等待连接数量下降，为false直接报错处理
        self.maxUsage = 100     #maxusage:单个连接的最大重复使用次数
        self.setSession = None
        self.reset = True


# ---- 用连接池来返回数据库连接
class DMysqlPoolConn:

    __pool = None
    def __init__(self, config):
        if not self.__pool:
            self.__class__.__pool = PooledDB(creator=pymysql,
                                             maxconnections=config.maxConnection,
                                             mincached=config.minCached,
                                             maxcached=config.maxCached,
                                             maxshared=config.maxShared,
                                             blocking=config.blocking,
                                             maxusage=config.maxUsage,
                                             setsession=config.setSession,
                                             charset=config.charset,
                                             host=config.host,
                                             port=config.port,
                                             database=config.db,
                                             user=config.user,
                                             password=config.password,
                                             )

    def get_conn(self):
        return self.__pool.connection()

#***********自定义填写数据库配置*****
host = 'localhost'
port = 3306
user = 'root'
password = '512xzhXZH'
db = 'ar'

db_config = DMysqlConfig(host, db, user, password, port)
g_pool_connection = DMysqlPoolConn(db_config)


# ---- 调用时，使用 with 的方式来优化代码
class UsingMysql(object):

    def __init__(self, commit=True, log_time=True, log_label='总用时'):
        """
        :param commit: 是否在最后提交事务(设置为False的时候方便单元测试)
        :param log_time:  是否打印程序运行总时间
        :param log_label:  自定义log的文字
        """
        self._log_time = log_time
        self._commit = commit
        self._log_label = log_label

    def __enter__(self):
        # 如果需要记录时间
        if self._log_time is True:
            self._start = default_timer()

        # 从连接池获取数据库连接
        conn = g_pool_connection.get_conn()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        conn.autocommit = False     #控制是否自动提交数据库修改

        self._conn = conn
        self._cursor = cursor
        return self

    def __exit__(self, *exc_info):
        # 提交事务
        if self._commit:
            self._conn.commit()
        # 在退出的时候自动关闭连接和cursor
        self._cursor.close()
        self._conn.close()

        if self._log_time is True:
            diff = default_timer() - self._start
            print('-- %s: %.6f 秒' % (self._log_label, diff))

    # ************* 一系列封装的业务方法*************

    # 返回 count
    def get_count(self, sql, params=None, count_key='count(id)'):
        self.cursor.execute(sql, params)
        data = self.cursor.fetchone()
        print("--  get_count,执行成功,sql=", sql)
        if not data:
            return 0
        return data[count_key]

    #执行sql语句 增加，删除，更新
    def executeSql(self,sql,params=None):
        try:
            self.cursor.execute(sql,params)
            print("--  executeSql,执行成功,sql=",sql)
        except Exception:
            print("executeSql，Error,sql=",sql)

    #保护变量
    @property
    def cursor(self):
        return self._cursor

