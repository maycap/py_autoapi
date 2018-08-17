# coding: utf-8
from flask import Flask, request, jsonify
from werkzeug.wrappers import Response

from models import Base
from app import route_table, dispatch_table
from app.business import SqlCurd

app = Flask(__name__)

# 所有继承Base的表都允许查询
# 支持 id 以及任何可以作为唯一键的查询
@app.route('/api/models/<table>', methods=['GET'])
def support_query(table):
    if table.lower() in Base.metadata.tables.keys():
        select_table = Base.metadata.tables[table.lower()]
        curd_api = SqlCurd(select_table)
        params = request.args.to_dict()
        res = curd_api.__getattribute__(curd_api.method_map['get'])(**params)
        return jsonify(data=res)


# 可以配置，用来保证数据安全性
@app.route('/api/models/<table>', methods=['POST', 'PUT', 'DELETE'])
def support_method(table):
    response = Response()
    method = request.method.lower()
    table = table.lower()
    if table in route_table.keys() and dispatch_table(table, method):
        curd_api = SqlCurd(route_table[table])
        func = curd_api.__getattribute__(SqlCurd.method_map[method])
        if method in ['delete']:
            data = request.args.to_dict()
        else:
            data = request.json
        code, res = func(**data)
        response.status_code = code
        response.data = {'data': res}
        return response
    else:
        response.status_code = 405
        response.data = {'msg': u'方法暂不支持'}
        return response



