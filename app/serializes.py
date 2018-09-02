# coding: utf-8
from app.models import Base


class SerializeColumns(object):

    def __init__(self, table):
        self.table = self.return_model(table)

    def qeury_columns_attr(self):
        result = dict()
        for column in self.table.__table__.columns:
            result[column.name] = {
                'primary_key': column.primary_key,
                'type': column.type.python_type,
                'default': True if column.default else False,
                'unique': column.unique
            }
        return result

    @staticmethod
    def return_model(tablename):
        """
        返回model
        :return:
        """
        for model in Base.__subclasses__():
            if model.__tablename__ == tablename:
                return model
        return None

    @staticmethod
    def return_typeset(python_type):
        """
        一些类型属于同组
        :param python_type:
        :return:
        """
        if python_type == str:
            return (python_type, unicode)
        return (python_type)

    def match_columns(self, **kwargs):
        errors_type = dict()
        miss_primary = None
        miss_column = {}
        for column in self.table.__table__.columns:
            param = kwargs.get(column.name)
            if not param:
                if column.primary_key:
                    miss_primary = column.name
                # 对于有默认值的属性，没有传参的情况，直接跳过
                elif not column.default:
                    miss_column.update({
                        column.name: column.type.python_type.__name__
                    })
            else:
                # unicode 识别
                if not isinstance(param, self.return_typeset(column.type.python_type)):
                    if column.primary_key:
                        miss_primary = column.name
                    else:
                        errors_type.update({
                            column.name: 'Error: need {} but got {}'.format(
                                column.type.python_type.__name__, param.__class__.__name__)
                        })

        return miss_primary, miss_column, errors_type

    def restful_post_match_columns(self, **kwargs):
        """
        post除了主键外，都不可缺少
        :param kwargs:
        :return:
        """

        _, miss_column, errors_type = self.match_columns(**kwargs)


        print 'in check post', miss_column, errors_type

        if miss_column:
            return 400, 'Params {} is required!'.format(' '.join(miss_column.keys()))
        if errors_type:
            return 400, errors_type
        return 200, None

    def restful_put_match_columns(self, **kwargs):
        """
        全量修改，一个都不能少
        :param kwargs:
        :return:
        """
        miss_primary, miss_column, errors_type = self.match_columns(**kwargs)
        if miss_primary:
            return 400, 'Params <primary_key> {} is required!'.format(miss_primary)
        if miss_column:
            return 400, 'Params {} is required!'.format(' '.join(miss_column.keys()))
        if errors_type:
            return 400, errors_type
        return 200, None

    def restful_patch_match_columns(self, **kwargs):
        """
        局部修改：只要穿入的参数属性全对就行
        :param kwargs:
        :return:
        """
        miss_primary, _, errors_type = self.match_columns(**kwargs)
        if miss_primary:
            return 400, 'Params <primary_key> {} is required!'.format(miss_primary)
        if errors_type:
            return 400, errors_type
        return 200, None


    def restful_get_match_columns(self, **kwargs):
        """
        空函数
        :param kwargs:
        :return:
        """
        _, _, errors_type = self.match_columns(**kwargs)
        if errors_type:
            return 400, errors_type
        return 200, None

    def restful_delete_match_columns(self, **kwargs):
        """
        空函数
        :param kwargs:
        :return:
        """
        _, _, errors_type = self.match_columns(**kwargs)
        if errors_type:
            return 400, errors_type
        return 200, None

