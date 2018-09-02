# coding: utf-8
from functools import wraps

from flask import Flask, request, jsonify
from werkzeug.wrappers import Response

from app import route_setting
from app.business import SqlCurd
from app.serializes import SerializeColumns
from models import Base

app = Flask(__name__)

def decorated_route(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        response = Response()
        method = request.method.lower()
        path = request.path
        table = path.split('/')[3].lower()
        print 'path'
        if table not in Base.metadata.tables.keys():
            response.status_code = 404
            response.data = {'msg': u'model: {} not exist'.format(table)}
            return response

        if route_setting.get(table) and method not in route_setting.get(table):
            response.status_code = 405
            response.data = {'msg': u'model: {} not support method: {}'.format(table, method)}
            return response
        return func(*args, **kwargs)
    return decorated_function


# 获取可操作对象
@app.route('/api/models/', methods=['GET'])
def query_tables():
    return jsonify(data=Base.metadata.tables.keys())

@app.route('/api/models/<string:table>/<int:id>/', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
@decorated_route
def restful_primary_method(table, id):
    response = Response()
    method = request.method.lower()
    table = table.lower()

    match_api = SerializeColumns(table)
    if method in ['get', 'delete']:
        data = {"id": id}
    else:
        data = request.json if request.json else {}
        data.update({"id": id})
    code, res = match_api.__getattribute__('restful_{}_match_columns'.format(method))(**data)
    if code != 200:
        response.status_code = code
        response.data = res
        return response

    curd_api = SqlCurd(match_api.table)
    code, res = curd_api.__getattribute__(curd_api.method_map[method])(**data)
    response.status_code = code
    response.data = res
    return response

@app.route('/api/models/<string:table>/', methods=['POST'])
@decorated_route
def restful_post_method(table):
    response = Response()
    method = request.method.lower()
    table = table.lower()

    match_api = SerializeColumns(table)
    data = request.json if request.json else {}
    code, res = match_api.__getattribute__('restful_{}_match_columns'.format(method))(**data)
    if code != 200:
        response.status_code = code
        response.data = res
        return response

    curd_api = SqlCurd(match_api.table)
    ret, res = curd_api.__getattribute__(curd_api.method_map[method])(**data)
    response.status_code = code
    response.data = res
    return response




