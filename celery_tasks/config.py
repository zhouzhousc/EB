#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/24 11:06
# @Author  : userzhang
"""celery配置"""

broker_url = 'redis://127.0.0.1:6379/5'
broker_pool_limit = 1000  # Borker 连接池, 默认是10

timezone = 'Asia/Shanghai'
accept_content = ['pickle', 'json']

task_serializer = 'pickle'
result_expires = 3600  # 任务过期时间

result_backend = 'redis://127.0.0.1:6379/4'
result_serializer = 'pickle'
result_cache_max = 10000  # 任务结果最大缓存数量

worker_redirect_stdouts_level = 'INFO'

