#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/6 11:22
# @Author  : userzhang

# 使用celery

# sys.path.append('../')
# from apps.wangguang.models import SysInfo

import datetime
import json
import time

import requests
from celery import Celery
from django.conf import settings
# from django.template import loader, RequestContext
import os, django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edgebox_web.settings')
# django.setup()
# from celery.utils.log import get_task_logger
from django.utils import timezone
from celery_tasks.Core.send_email import EmailManage
from celery_tasks.Core.auth_corepro import AuthCorepro
from celery_tasks.Core.mqtt_pub_sub import mqtt_client_connect
from django_redis import get_redis_connection

# logger = get_task_logger('collect_log')
# logger.info('Refresh task start and refresh success')
# 创建一个Celery类的实例对象
app=Celery("celery_tasks.tasks", broker="redis://127.0.0.1:6379/0", backend="redis://127.0.0.1:6379/2")

# 解决时区问题,定时任务启动就循环输出
app.now = timezone.now




@app.task
def agent_sys_init():
    '''读取网关系统参数数据'''
    from apps.wangguang.models import SysInfo, RegisterInfo
    n=10
    while n:
        data=SysInfo.objects.create(sys_hostname="F1335086-BEACON",
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
        data=RegisterInfo.objects.create(gateway_name="EdgeBox003",
                                         gateway_id="6553791093879608705",
                                         gateway_secret="e3f3eeb045f0a19284ad03f64e101ce3f7fa15d135a7140e411fa29dbd269d7c",
                                         gateway_subdevice_num=0,
                                         gateway_model="IoT",
                                         gateway_trade_name="IoT",
                                         gateway_registration_time=datetime.datetime.now(),
                                         gateway_location="E5-4F",
                                         gateway_reset_time=datetime.datetime.now(),
                                         gateway_remark="EdgeBox边缘层网关测试版")

        data.save()
        # print("写入成功")
        print("写入成功")
        time.sleep(3)
        n=n-1



@app.task
def agent_to_corepro(types="CorePro", data_api=None, agent_name=None , agent_id=None,
                     agent_secret=None, agent_url=None, to_topic=None, seconds=3,):

    if types == "CorePro":
        if not all([data_api, agent_id, agent_name, agent_secret, agent_url, to_topic]):
            print("数据不完整")
        else:
            agent=AuthCorepro(DeviceName=agent_name,
                              ProductKey=agent_id,
                              DeviceSecret=agent_secret,
                              auth_url=agent_url)
            if agent.username == "":
                return False
            # # print(agent.username, agent.password, agent.mqtthost, agent.mqttport)
            # timestamp = str(round(time.time() * 1000))
            # mqttclient = mqtt_client_connect(broker= agent.mqtthost , port= int(agent.mqttport),
            #                                  username= agent.username , password= agent.password,
            #                                  client_id= timestamp)
            # time.sleep(1) #等待连接成功
            # mqttclient.mqttc.subscribe(to_topic+'/reply')
            # time.sleep(1) #等待订阅成功
            # # 跳过系统代理
            # session = requests.Session()
            # session.trust_env = False
            # r=session.get(url=data_api)
            # if r.status_code==200:
            #     data_list=r.json()
            #     for data in data_list:
            #         temp = {
            #             "system_params": {
            #                 "appid": "datakeyNqxn0hlClNe3MSP7UFn2",  # 数据类型id 变动
            #                 "timestamp": time.time(),
            #                 "type": "",
            #                 "token": "",
            #                 "sign": "",
            #                 "messageid": str(int(time.time()))
            #             },
            #             "app_params": []
            #         }
            #         message=eval(data["data"])
            #         temp["app_params"].append(message)
            #         payload = json.dumps(temp, ensure_ascii=False)
            #         mqttclient.mqttc.publish(topic=to_topic, payload=payload)
            #         time.sleep(seconds)

            # mqttclient.mqttc.loop_stop() #停止client循环
            # mqttclient.mqttc.disconnect() #干净的断开连接

            while 1:
                time.sleep(200)
                break
            return True


# 定义任务函数 注册用户时发送Email
@app.task
def send_register_active_email(receiver, subject, html_message):

    ''' 发送激活邮件 '''
    EmailManage.sendMail(receiver, subject, html_message)
    return True



@app.task
def transmit_for_mqtt(count_key, subdevice_key, transmit_key, transmit_ip,transmit_port,transmit_username,transmit_password,transmit_topic):
    '''转发至mqtt'''
    print(count_key, subdevice_key, transmit_key, transmit_ip, transmit_port, transmit_username, transmit_password, transmit_topic)
    subdevice_id=subdevice_key.split("_")[-1]
    transmit_id=transmit_key.split("_")[-1]
    status_key = "transmit_status_%d_%d" % (int(subdevice_id), int(transmit_id))
    conn = get_redis_connection('default')

    while 1:
        # 连接MQTT超时网络不通状况下循环 连接成功退出循环
        timestamp = str(round(time.time() * 1000))
        mqttclient = mqtt_client_connect(broker=transmit_ip,
                                         port=int(transmit_port),
                                         username=transmit_username,
                                         password=transmit_password,
                                         client_id=timestamp)

        if mqttclient.flag==0:
            # mqtt客户端连接不上 或网络不通 想自动连接
            conn.set(status_key,"连接MQTT超时")
            print(subdevice_id +transmit_id+ "连接MQTT超时")
            time.sleep(.5)
            if int(conn.get(subdevice_key).decode()) and int(conn.get(transmit_key).decode()):
                break
            else:
                continue
        else:
            break

    transmit_count = int(conn.get(count_key).decode())
    # session = requests.session()
    # session.trust_env = False  # 不使用系统全局代理

    proxies = {"http": "", "https": "", } # 不使用系统全局代理
    headers = {'Connection': 'close'} #在短时间使用多次requests.get
    while True:
        # data = session.get(url="http://127.0.0.1:9090/apidata/notsend/%s"%subdevice_id)
        data = requests.get(url="http://127.0.0.1:9090/apidata/notsend/%s"%subdevice_id,
                            proxies=proxies, headers=headers)
        if data.status_code==200:
            device_datas=data.json()
            if len(device_datas)==0:
                conn.set(status_key, "设备无数据")
                print(subdevice_id+transmit_id+"设备无数据")
                time.sleep(.5)
            for device_data in device_datas:
                if int(conn.get(subdevice_key).decode()) and int(conn.get(transmit_key).decode()):
                    # print(type(device_data),device_data["data"])
                    mqttclient.mqttc.publish(topic=transmit_topic, payload=device_data["data"],qos=1)
                    transmit_count=transmit_count+1
                    conn.set(count_key, transmit_count)
                    conn.set(status_key, "正在运行")
                    time.sleep(1.5)
                else:
                    break
        if int(conn.get(subdevice_key).decode()) and int(conn.get(transmit_key).decode()):
            # 传输程序跳出来后 再次判断设备和传输是否启动
            continue
        else:
            if int(conn.get(subdevice_key).decode())==0:
                # 设备被禁用 陷入假循环
                conn.set(status_key, "设备被禁用")
                print(subdevice_id+transmit_id+"设备被禁用")
                time.sleep(.5)
                continue
            if int(conn.get(transmit_key).decode()) == 0:
                # 传输通道关闭 程序终止
                print(subdevice_id+transmit_id+"转发停止")
                mqttclient.mqttc.loop_stop()
                mqttclient.mqttc.disconnect()
                break

    # print(transmit_ip)



@app.task
def transmit_for_corepro(count_key, subdevice_key, transmit_key, device_name,device_id,device_secret):
    '''转发至mqtt'''
    print(count_key, subdevice_key, transmit_key, device_name, device_id, device_secret)
    subdevice_id=subdevice_key.split("_")[-1]
    transmit_id=transmit_key.split("_")[-1]
    status_key = "transmit_status_%d_%d" % (int(subdevice_id), int(transmit_id))
    conn = get_redis_connection('default')

    while 1:
        # 鉴权通道
        auth_url = "http://service-de8elrpo-1255000335.apigw.fii-foxconn.com/release/corepro/auth/mqtt/?X-NameSpace-Code=corepro&X-MicroService-Name=corepro-device-auth"
        agent = AuthCorepro(DeviceName=device_name,
                            ProductKey=device_id,
                            DeviceSecret=device_secret,
                            auth_url=auth_url)
        print(agent.username, agent.password, agent.mqtthost, agent.mqttport)
        transmit_ip = agent.mqtthost
        transmit_port = agent.mqttport
        transmit_username = agent.username
        transmit_password = agent.password
        transmit_topic='/%s/%s/property/post'% (device_id,device_name)
        transmit_topic_reply='/%s/%s/property/post/reply'% (device_id,device_name)
        # 连接MQTT超时网络不通状况下循环 连接成功退出循环
        timestamp = str(round(time.time() * 1000))
        mqttclient = mqtt_client_connect(broker=transmit_ip,
                                         port=int(transmit_port),
                                         username=transmit_username,
                                         password=transmit_password,
                                         client_id=timestamp)
        mqttclient.mqttc.subscribe(topic=transmit_topic_reply)
        if mqttclient.flag==0:
            # mqtt客户端连接不上 或网络不通 想自动连接
            conn.set(status_key,"连接MQTT超时")
            print(subdevice_id +transmit_id+ "连接MQTT超时")
            time.sleep(1.5)
            if int(conn.get(subdevice_key).decode()) and int(conn.get(transmit_key).decode()):
                break
            else:
                continue
        else:
            break

    transmit_count = int(conn.get(count_key).decode())
    # session = requests.session()
    # session.trust_env = False  # 不使用系统全局代理

    proxies = {"http": "", "https": "", } # 不使用系统全局代理
    headers = {'Connection': 'close'} #在短时间使用多次requests.get

    while True:
        # data = session.get(url="http://127.0.0.1:9090/apidata/notsend/%s"%subdevice_id)
        data = requests.get(url="http://127.0.0.1:9090/apidata/notsend/%s"%subdevice_id,
                            proxies=proxies, headers=headers)
        if data.status_code==200:
            device_datas=data.json()
            if len(device_datas)==0:
                conn.set(status_key, "设备无数据")
                print(subdevice_id+transmit_id+"设备无数据")
                time.sleep(.5)
            for device_data in device_datas:
                if int(conn.get(subdevice_key).decode()) and int(conn.get(transmit_key).decode()):
                    # print(type(device_data),device_data["data"])
                    data_format = {
                        "params": {
                            "humidity": 0,
                            "current": 0,
                            "temperature": 0
                        },
                        "msg_ver": int(time.strftime("%Y%m%d%H%M%S")),
                        "id": str(time.time())
                    }
                    data_format["params"]=json.loads(device_data["data"])
                    mqttclient.mqttc.publish(topic=transmit_topic, payload=json.dumps(data_format),qos=1)
                    transmit_count=transmit_count+1
                    conn.set(count_key, transmit_count)
                    conn.set(status_key, "正在运行")
                    time.sleep(2.5)
                else:
                    break
        if int(conn.get(subdevice_key).decode()) and int(conn.get(transmit_key).decode()):
            # 传输程序跳出来后 再次判断设备和传输是否启动
            continue
        else:
            if int(conn.get(subdevice_key).decode())==0:
                # 设备被禁用 陷入假循环
                conn.set(status_key, "设备被禁用")
                print(subdevice_id+transmit_id+"设备被禁用")
                time.sleep(.5)
                continue
            if int(conn.get(transmit_key).decode()) == 0:
                # 传输通道关闭 程序终止
                print(subdevice_id+transmit_id+"转发停止")
                mqttclient.mqttc.loop_stop()
                mqttclient.mqttc.disconnect()
                break

    # print(transmit_ip)










