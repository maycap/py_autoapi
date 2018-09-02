# coding: utf-8
import datetime

from app.models import Session


def row2dict(row):
    d = dict()
    for key in row.__table__.columns:
        value = getattr(row, key.name)
        if isinstance(key.type.python_type, datetime.datetime):
            d[key.name] = value.strftime("%Y-%m-%d %H:%M:%S")
        else:
            d[key.name] = value
    return d

class SqlCurd(object):

    method_map = {
        'get': 'query',
        'post': 'create',
        'put': 'update',
        'delete': 'delete',
        'patch': 'update',
    }

    def __init__(self, table):
        self.table = table

    def get_unique_key(self):
        """
        获取主键
        :return:
        """
        keys = []
        if hasattr(self.table, 'columns'):
            columns = self.table.columns
        else:
            columns = self.table.__table__.columns
        for column in columns:
            if column.unique and not column.nullable:
                keys.append(column.name)
        return keys

    def modify_raw(self, raw, data):
        """
        修改数据
        :param raw:
        :param data:
        :return:
        """
        print raw, data
        for key in data:
            if hasattr(raw, key):
                setattr(raw, key, data[key])

    def create(self, **data):
        """
        create
        :param data:
        :return:
        """
        with Session() as ss:
            query = self.table()
            self.modify_raw(query, data)
            ss.add(query)
            ss.flush()
            ss.commit()
            return 200, query.id

    def update(self, **data):
        """
        update
        :param data:
        :return:
        """
        # 基于 id 的更新
        cid = data.pop('id', -1)
        with Session() as ss:
            if cid > 0:
                query = ss.query(self.table).filter(self.table.id == cid).first()
                if query:
                    self.modify_raw(query, data)
                    ss.add(query)
                    ss.commit()
                    return 200, query.id
                return 404, u'id无法关联信息'

            # 基于其他唯一且不为空的key更新
            keys = self.get_unique_key()
            for key in keys:
                name = data.pop(key, None)
                if name:
                    query = ss.query(self.table).filter(self.table.__dict__[key] == name).first()
                    if query:
                        self.modify_raw(query, data)
                        ss.add(query)
                        ss.commit()
                        return 200, query.id
            return 404, u'没有匹配到任何行'

    def query(self, **kwargs):
        """
        query
        :return:
        """
        result = []
        with Session() as ss:
            query = ss.query(self.table)
            for key in kwargs:
                if hasattr(self.table, key):
                    query = query.filter(self.table.__dict__[key] == kwargs[key])
            for item in query:
                result.append(row2dict(item))
            return 200, result

    def delete(self, id=None):
        """
        删除
        :param id:
        :return:
        """
        if not id:
            return 200, 'nothing need to delete'
        with Session() as ss:
            ss.query(self.table).filter(self.table.id == id).\
                delete(synchronize_session=False)
            return 200, 'delete {} done'.format(id)


