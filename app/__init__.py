# coding: utf-8
'''
简单路由设置：
1、get请求默认全允许
2、其他方法读取当前配置，默认全允许
'''

from sqlalchemy.ext.declarative import DeclarativeMeta
from app import models


# 单独指定 User表 只允许，查询、新增、更新，（不允许删除）
# 表名请使用小写
route_setting = {
    'path': ['models'],             # 数据库模块地址
    'user': ['post', 'put'],
}


# 注入table路由，用来不区分大小写
route_table = {}
for path in route_setting['path']:
    for method in dir(models):
        if isinstance(getattr(models, method), DeclarativeMeta) and hasattr(getattr(models, method), '__tablename__'):
            route_table.update({getattr(models, method).__tablename__: getattr(models, method)})


# 路由方法过滤
def dispatch_table(tablename, method):
    if not route_setting.get(tablename):
        return True
    if method in route_setting[tablename]:
        return True
    return False

