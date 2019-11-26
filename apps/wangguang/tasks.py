#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/31 16:24
# @Author  : userzhang
import datetime

import time
from celery.task import Task
import django
django.setup()
from .models import SysInfo, RegisterInfo



class Agent_sys_init_tasks(Task):
    name = "Agent_sys_init_tasks"


    def run(self, *args, **kwargs):
        '''读取网关系统参数数据'''
        print("start Agent sys task")
        data = SysInfo.objects.create(sys_hostname="F1335086-BEACON",
                                      sys_product_name="边缘层智能网关",
                                      sys_os="Microsoft Windows 7 旗舰版",
                                      sys_ip="10.167.198.111",
                                      sys_mac="70-20-84-30-EE-83",
                                      sys_mask="255.255.252.0",
                                      sys_gateway="10.167.196.1",
                                      sys_net_status=0,
                                      sys_rateof_cpu="50%",
                                      sys_memory="3.2G",
                                      sys_memory_size="8.2G",
                                      sys_harddisk="1300G",
                                      sys_harddisk_size="2000G",
                                      sys_usb_num=4,
                                      sys_rs232_num=6,
                                      sys_running_time="0秒",
                                      sys_local_time=datetime.datetime.now(),
                                      sys_out_time=datetime.datetime.now(),
                                      sys_net_model="HTTP/MQTT")
        data.save()
        data = RegisterInfo.objects.create(gateway_name="EdgeBox003",
                                           gateway_key="6553791093879608705",
                                           gateway_secret="e3f3eeb045f0a19284ad03f64e101ce3f7fa15d135a7140e411fa29dbd269d7c",
                                           gateway_subdevice_num=0,
                                           gateway_model="IoT",
                                           gateway_trade_name="IoT",
                                           gateway_registration_time=datetime.datetime.now(),
                                           gateway_location="E5-4F",
                                           gateway_reset_time=datetime.datetime.now(),
                                           gateway_remark="EdgeBox边缘层网关测试版")

        data.save()
        print("写入成功")
        print("end Agent sys task")

