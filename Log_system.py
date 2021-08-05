# -*- coding: utf-8 -*-
# @Time : 2021/8/5 9:19
# @Author : 谢泽辉
# @Software : PyCharm

import time

#LogText:需要记录的数据
def writeLog(LogText=''):
    # 格式化成2021-08-05 09:42:08形式
    time_true = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    filename = "./Log.txt"
    with open(filename, 'a+',encoding="utf8") as f:
        f.writelines([time_true,"   ",LogText+"\n"] )

