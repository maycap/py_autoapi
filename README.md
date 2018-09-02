# web自动CURD

### 版本
	
* 1.1

### 前言

动动手设计下表结构，就能自动注入对应API方法；

基于sqlalchemy 与flask框架实现的数据库模块自动生成CURD demo



### 使用介绍


	# 默认为测试sqlite，初始化数据库
	python manager.py init_db		
	
	# 启动服务，默认端口 5000	
	python manager.py run
	
	# 只需要在app/models.py 中定义 Table，会自动注入CURD API方法
	添加新表，需要重新 init_db
	

### 方法介绍

> 获取对象列表

	GET http://127.0.0.1:5000/api/models/
	
> 获取一个对象
	
	GET http://127.0.0.1:5000/api/models/<string:table>/<int:id>/
	
> 创建一个对象

	POST http://127.0.0.1:5000/api/models/<string:table>/

> 修改一个对象

	PUT http://127.0.0.1:5000/api/models/<string:table>/<int:id>/
	
> 修改部分属性一个对象

	PATCH http://127.0.0.1:5000/api/models/<string:table>/<int:id>/

> 删除一个对象
	
	DELETE http://127.0.0.1:5000/api/models/<string:table>/<int:id>/	


### 修改与新增功能列表

* 提取模块校验为装饰器，统一 404、405 返回
* 修改为了restful api格式
* 统一使用Base管理所有子类，避免导入model
* 添加字段类型校验功能（默认值智能校验）

### 后续

	提供api doc，生成在线文档

