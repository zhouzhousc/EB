#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/8 15:00
# @Author  : userzhang
import json
import time
import threading
from celery import Celery
from celery.utils.log import get_task_logger
logger = get_task_logger('gateway_log')
logger.info('Refresh task start and refresh success')

app1=Celery("celery_tasks.tasks_timing", broker="redis://127.0.0.1:6379/0", backend="redis://127.0.0.1:6379/2")
import serial.tools.list_ports
import serial
from django_redis import get_redis_connection
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edgebox_web.settings')
django.setup()

confirm_port = []  # 已经握手确定的串口号 不需要再重新确认

def m5_open_write(com, botelv, conn, device):
    time.sleep(0.5)
    try:
        # 1. 打开端口
        with serial.Serial(com, baudrate=botelv, timeout=3) as ser:
            a=b=0
            while ser.isOpen():
                time.sleep(0.1)

                data = ''
                data = data.encode()
                n = ser.inWaiting()
                if n:
                    # data = data+ser.read(n)
                    data = data+ser.readline()
                # n = ser.inWaiting()
                if len(data) > 1:
                    b=0
                    a=a+1
                    if a==1:
                        print("第一条消息不全丢掉")
                    else:
                        # 2. 读取数据
                        print(data.decode("gb2312"))
                        # 3. 写入设备API

                        # print(data)

                else:
                    # 计数120次就默认没有消息上来 退出循环
                    # print(b)
                    b=b+1
                    if b==120:
                        conn.delete(device)
                        print("break")
                        break
    except Exception as e:
        print(str(e)+"11111")
        conn.delete(device)
        print("break")

def is_json(json_str):
    try:
        json.loads(json_str)
        return True
    except :
        return False


# 扫描有回指令的端口号
def scanfPort(redis_com_list,conn):
    portList = list(serial.tools.list_ports.comports())
    for i in portList:
        try:
            if i[0] not in redis_com_list:
                # 判断未曾确认的端口
                #已经打开的端口 语句会报错
                # serialFd = serial.Serial(port=i[0], baudrate=9600, timeout=3)
                with serial.Serial(i[0], baudrate=9600, timeout=3) as ser:
                    if ser.isOpen():
                        print(i[0]+" is open success")
                        # 发送握手信息
                        ser.write(b"PING")

                        json_str=ser.readline().decode("gb2312").strip("\r\n")
                        if is_json(json_str):
                            # 确认符合
                            head=json.loads(json_str)
                            #握手成功！！！
                            print(i[0] + " 握手成功！！！")
                            m5device_name=head["m5device_name"]
                            m5device_type=head["m5device_type"]
                            m5device_com=i[0]
                            m5device_botelv="9600"
                            m5device_remark=head["m5device_remark"]
                            m5device_forward=head["m5device_forward"]
                            # redis_com_list.append(i[0])
                            # 握手成功 添加在redis 中
                            conn.hset("m5_%s"%m5device_name, "m5device_name", m5device_name)
                            conn.hset("m5_%s"%m5device_name, "m5device_type", m5device_type)
                            conn.hset("m5_%s"%m5device_name, "m5device_com", m5device_com)
                            conn.hset("m5_%s"%m5device_name, "m5device_botelv", m5device_botelv)
                            conn.hset("m5_%s"%m5device_name, "m5device_remark", m5device_remark)

                            for index, path in enumerate(m5device_forward):
                                conn.hset("m5path_%s_%d" % (m5device_name, index), "m5path_name", path["path_name"])
                                conn.hset("m5path_%s_%d" % (m5device_name, index), "m5path_type", path["path_type"])
                                conn.hset("m5path_%s_%d" % (m5device_name, index), "m5path_ip", path["path_ip"])
                                conn.hset("m5path_%s_%d" % (m5device_name, index), "m5path_port", path["path_port"])
                                conn.hset("m5path_%s_%d" % (m5device_name, index), "m5path_user", path["path_user"])
                                conn.hset("m5path_%s_%d" % (m5device_name, index), "m5path_pwd", path["path_pwd"])
                                conn.hset("m5path_%s_%d" % (m5device_name, index), "m5path_topic", path["path_topic"])
                                conn.hset("m5path_%s_%d" % (m5device_name, index), "m5path_remark", path["path_remark"])

                                conn.hset("m5path_%s_%d" % (m5device_name, index), "m5path_enable", '启用')# 默认启用
                                conn.hset("m5path_%s_%d" % (m5device_name, index), "m5path_count", 0)# 计数
                                conn.hset("m5path_%s_%d" % (m5device_name, index), "m5path_status", "正在运行")# 状态
                            # delay tasks 任务 (打开串口 读取数据 写入设备API)
                            # m5_open_write.delay(i[0],int(m5device_botelv))
                            # print(i[0] + " " + m5device_botelv + " delay")
                            mythread = threading.Thread(target=m5_open_write, args=(i[0], 9600, conn,"m5_%s"%m5device_name))
                            mythread.setDaemon(True)
                            mythread.start()

                print(i[0]+ " is close")

            else:
                print("no found ")
                time.sleep(1)
        except Exception as e:
            print(i[0]+" is open fail"+str(e))
            time.sleep(1)



@app1.task
def m5ScanfPorts():
    conn = get_redis_connection('default')
    print(m5ScanfPorts.request.id)

    m5_key = "m5_*"
    while True:
        redis_com_list = {"COM1","COM2","COM3"}
        # s搜索缓存所有可用的端口号
        m5s = conn.keys(m5_key)
        # print(m5s)
        try:
            # 有可能在遍历m5_devices时 设备就已经拔掉 rasie KeyError
            for m5 in m5s:
                b_info=conn.hgetall(m5.decode())
                info={}
                for i,value in b_info.items():
                    info[i.decode()]=value.decode("utf-8")
                # 添加至redis_com_list 集合中
                redis_com_list.add(info["m5device_com"])
        except Exception as e:
            print(str(e)+"22222")
        # time.sleep(3)
        print("redis_com_list"+str(redis_com_list))
        scanfPort(redis_com_list,conn)





@app1.task
def gateway_status_message():
    '''网关状态定时发布'''
    data={"status": "200", "devices": 20}
    print(data)