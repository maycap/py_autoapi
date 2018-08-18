# web自动CURD

### 前言

基于sqlalchemy 与flask框架实现的数据库模块自动生成CURD demo

### 使用介绍


	# 默认为测试sqlite，初始化数据库
	python manager.py init_db		
	
	# 启动服务，默认端口 5000	
	python manager.py run				


### 方法介绍

> get

	原理： 基于Base父类获取，如果单独使用无需注入路由等配置；
	策略： 默认全部开启
	支持： 所有表字段

> post | put

	原理： 基于ORM模块
	策略： 默认全部开启，可在__init__中配置
	支持： id、以及所有设置为 unique 关键字的更新

> delete

	原理： 同 post
	策略： 同 post
	支持： 仅支持id方法删除

### 备注

* 采用Base父类，可以省去路由注入等很多操作，缺点只可读；适合全表管理，比如：创建、自动化前端表格创建

### 后续

* 表字段自动类型校验

