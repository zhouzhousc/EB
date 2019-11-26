#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/15 14:37
# @Author  : userzhang
# from celery_tasks.tasks import send_register_active_email, agent_to_corepro, agent_sys_init
import json

from celery_tasks.tasks_timing import m5ScanfPorts,app1
task=m5ScanfPorts.delay()
print(task)

#1) "celery-task-meta-89d4ecb8-af6b-45d2-9a46-5a6934a18418"
# 2) "celery-task-meta-a6059c8b-f31f-41ae-93ba-86a26261a526"
# 3) "celery-task-meta-75643031-b304-443b-9ff1-ff6ba0c22470"
# 4) "celery-task-meta-511c6e49-e547-4505-b193-e1765ea53e98"
# app1.control.revoke('22661016-4a02-4af9-a2c9-f7ecda30ef61',terminate=True )
# from django.utils.autoreload import *
# try:
#     # agent_to_corepro.delay(data_api="http://127.0.0.1:9090/apidata/notsend/6",
#     #                    agent_id="6553791093879608705",
#     #                    agent_name="EdgeBox003",
#     #                    agent_secret="e3f3eeb045f0a19284ad03f64e101ce3f7fa15d135a7140e411fa29dbd269d7c",
#     #                    to_topic="/data/6553791093879608705/testdata/data/gateway",
#     #                    agent_url="http://service-de8elrpo-1255000335.apigw.fii-foxconn.com/release/corepro/auth/mqtt/?X-NameSpace-Code=corepro&X-MicroService-Name=corepro-device-auth")
#     agent_to_corepro.delay(data_api="http://127.0.0.1:9090/apidata/notsend/7",
#                        agent_id="6554066342204904220",
#                        agent_name="gateway05",
#                        agent_secret="341f01b2f8ac031d1ee37dae77a94471209737ba40f8308bdf9a6a24e9ab5f40",
#                        to_topic="/data/6553791093879608705/testdata/data/gateway",
#                        agent_url="http://coreproapi.fiibeacon.com/release/corepro/auth/mqtt_auth?X-MicroService-Name=corepro-device-auth&X-NameSpace-Code=corepro")
# except Exception as e:
#     print(e)
# agent_sys_init.delay()

import threading


# 这是你写的监控函数
import time
#
#
# def monitor(name):
#     print("数据转发"+name)
#     time.sleep(3)
#
#
# def control_monitor(enable,name):
#     # with threading.Lock():
#     while enable:
#         monitor(name)
#     if enable:
#         print('开启完成')
#     else:
#         print('关闭完成')
#
# control_monitor(True, 'liu')
# control_monitor(True, 'zhang')

# a=b'dwew'
# print(type(a),a)
# a=a.decode()
# print(type(a),a)

# a=[81, 33, 0, '0']
# if not all(a):
#     print(1)
# else:
#     print(2)

# import requests
# session=requests.Session()
# session.trust_env=False
# # 转发模块从设备api拿到未发送的数据 开始循环 发送每条记录
# # http://127.0.0.1:<port>/apidata/notsend/<subdevice_id>
# data=session.get(url="http://127.0.0.1:9090/apidata/notsend/1")
# print(data.json())

# strcurtime = int(time.strftime("%Y%m%d%H%M%S"))
# print(int(strcurtime))
# from numba import jit
# import time
#
# def foo(x,y):
#     tt = time.time()
#     s=0
#     for i in range(x,y):
#         s += i
#     print("Time used: {} sec".format(time.time()-tt))
#     return s
#
# print(foo(1,100000000))
# import serial
# import serial.tools.list_ports
#
# confirm_port = []  # 已经握手确定的串口号 不需要再重新确认
#
#
# def scanfPort():
#     portList = list(serial.tools.list_ports.comports())
#     for i in portList:
#         try:
#             if i[0] not in confirm_port :
#                 # 判断未曾确认的端口
#                 #已经打开的端口 语句会报错
#                 serialFd = serial.Serial(port=i[0], baudrate=9600, timeout=3)
#                 if serialFd.isOpen():
#                     print(i[0],"is open success")
#                     # 发送握手信息
#                     confirm_port.append(i[0])
#                     # 握手成功 添加在redis 中
#                 serialFd.close()
#                 print(i[0], "is close")
#             else:
#                 print("no found ")
#                 time.sleep(1)
#         except Exception as e:
#             print(i[0], "is open fail")
#             time.sleep(1)
#
#     print("confirm_port:", confirm_port)
#
#
# while True:
#     scanfPort()
