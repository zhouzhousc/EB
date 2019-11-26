#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/31 16:08
# @Author  : userzhang
from datetime import timedelta

import djcelery

djcelery.setup_loader() #

BROKER_BACKEND = "redis"
BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/2"

CELERY_QUEUES = {
    "beat_queue" : {
        "exchange" : "beat_queue",
        "exchange_type" : "direct",
        "binding_key" : "beat_queue"
    },
    "worker_queue" : {
        "exchange" : "worker_queue",
        "exchange_type" : "direct",
        "binding_key" : "worker_queue"
    }
}

CELERY_DEFAULT_QUEUE = "worker_queue"  # 设定默认队列


# 确认的app任务列表
CELERY_IMPORTS = (
    'apps.wangguang.tasks',  #网关实时更新系统信息任务
    'apps.user.tasks',  #用户注册发送邮箱任务
    'apps.m5.tasks', #扫描M5智能硬件任务
    'apps.shebei.tasks', #设备转发模块
    'apps.qudong.tasks', #设备采集驱动模块
    'apps.loginfo.tasks', #日誌模块
)


# 有些情况防止死锁
CELERYD_FORCE_EXECV = True

# 设置并发的worker数量
CELERYD_CONCURRENCY = 5


# 允许重试
# CELERY_ACKS_LATE = True


# 每个worker最多执行100个任务被销毁
CELERYD_MAX_TASKS_PER_CHILD = 100


# 单个任务最大运行时间
# CELERYD_TASK_TIME_LIMIT = 12 * 30

TIME_ZONE = 'Asia/Shanghai'



CELERYBEAT_SCHEDULE = {
    # "agent_sys_init" : {
    #     "task" : "Agent_sys_init_tasks",
    #     "schedule": timedelta(seconds=5),
    #     # "args":("tasks","beat"),
    #     "options":{
    #         "queue": "beat_queue"
    #
    #     }
    # },
    "m5_scanf":{
        "task" : "M5_scanf_tasks",
        "schedule" : timedelta(seconds=20),
        "options":{
            "queue": "beat_queue"
        }
    },
    "drive_modebusrtu":{
        "task" : "Drive_modebusrtu",
        "schedule" : timedelta(seconds=10),
        "options":{
            "queue": "beat_queue"
        }
    }


}

