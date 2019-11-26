# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # @Time    : 2019/8/31 17:18
# # @Author  : userzhang
import json

import time

import requests
from celery.task import Task
import django
django.setup()
from django_redis import get_redis_connection
from .Core.auth_corepro import AuthCorepro
from .Core.mqtt_pub_sub import mqtt_client_connect


class transmit_for_mqtt(Task):
    name = "transmit_for_mqtt"

    def run(self,count_key, subdevice_key, transmit_key, transmit_ip,transmit_port,transmit_username,transmit_password,transmit_topic):
        print(count_key, subdevice_key, transmit_key, transmit_ip, transmit_port, transmit_username, transmit_password,
              transmit_topic)
        subdevice_id = subdevice_key.split("_")[-1]
        transmit_id = transmit_key.split("_")[-1]
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

            if mqttclient.flag == 0:
                # mqtt客户端连接不上 或网络不通 想自动连接
                conn.set(status_key, "连接MQTT超时")
                print(subdevice_id + transmit_id + "连接MQTT超时")
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

        proxies = {"http": "", "https": "", }  # 不使用系统全局代理
        headers = {'Connection': 'close'}  # 在短时间使用多次requests.get
        while True:
            # data = session.get(url="http://127.0.0.1:9090/apidata/notsend/%s"%subdevice_id)
            with requests.Session() as s:
                s.keep_alive = False
                data = s.get(url="http://127.0.0.1:9090/apidata/notsend/%s" % subdevice_id,
                                    proxies=proxies, headers=headers)
                if data.status_code == 200:
                    device_datas = data.json()
                    if len(device_datas) == 0:
                        conn.set(status_key, "设备无数据")
                        print(subdevice_id + transmit_id + "设备无数据")
                        time.sleep(.5)
                    for device_data in device_datas:
                        if int(conn.get(subdevice_key).decode()) and int(conn.get(transmit_key).decode()):
                            # print(type(device_data),device_data["data"])
                            mqttclient.mqttc.publish(topic=transmit_topic, payload=device_data["data"], qos=1)
                            transmit_count = transmit_count + 1
                            conn.set(count_key, transmit_count)
                            conn.set(status_key, "正在运行")
                            time.sleep(1.5)
                        else:
                            break
            if int(conn.get(subdevice_key).decode()) and int(conn.get(transmit_key).decode()):
                # 传输程序跳出来后 再次判断设备和传输是否启动
                continue
            else:
                if int(conn.get(subdevice_key).decode()) == 0:
                    # 设备被禁用 陷入假循环
                    conn.set(status_key, "设备被禁用")
                    print(subdevice_id + transmit_id + "设备被禁用")
                    time.sleep(.5)
                    continue
                if int(conn.get(transmit_key).decode()) == 0:
                    # 传输通道关闭 程序终止
                    print(subdevice_id + transmit_id + "转发停止")
                    mqttclient.mqttc.loop_stop()
                    mqttclient.mqttc.disconnect()
                    break

        # print(transmit_ip)

class transmit_for_corepro(Task):
    name = "transmit_for_corepro"

    def run(self,count_key, subdevice_key, transmit_key, device_name,device_id,device_secret):
        print(count_key, subdevice_key, transmit_key, device_name, device_id, device_secret)
        subdevice_id = subdevice_key.split("_")[-1]
        transmit_id = transmit_key.split("_")[-1]
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
            transmit_topic = '/%s/%s/property/post' % (device_id, device_name)
            transmit_topic_reply = '/%s/%s/property/post/reply' % (device_id, device_name)
            # 连接MQTT超时网络不通状况下循环 连接成功退出循环
            timestamp = str(round(time.time() * 1000))
            mqttclient = mqtt_client_connect(broker=transmit_ip,
                                             port=int(transmit_port),
                                             username=transmit_username,
                                             password=transmit_password,
                                             client_id=timestamp)
            mqttclient.mqttc.subscribe(topic=transmit_topic_reply)
            if mqttclient.flag == 0:
                # mqtt客户端连接不上 或网络不通 想自动连接
                conn.set(status_key, "连接MQTT超时")
                print(subdevice_id + transmit_id + "连接MQTT超时")
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

        proxies = {"http": "", "https": "", }  # 不使用系统全局代理
        headers = {'Connection': 'close'}  # 在短时间使用多次requests.get

        while True:
            with requests.Session() as s:
                s.keep_alive = False
                # data = session.get(url="http://127.0.0.1:9090/apidata/notsend/%s"%subdevice_id)
                data = s.get(url="http://127.0.0.1:9090/apidata/notsend/%s" % subdevice_id,
                                    proxies=proxies, headers=headers)
                if data.status_code == 200:
                    device_datas = data.json()
                    if len(device_datas) == 0:
                        conn.set(status_key, "设备无数据")
                        print(subdevice_id + transmit_id + "设备无数据")
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
                            data_format["params"] = json.loads(device_data["data"])
                            mqttclient.mqttc.publish(topic=transmit_topic, payload=json.dumps(data_format), qos=1)
                            transmit_count = transmit_count + 1
                            conn.set(count_key, transmit_count)
                            conn.set(status_key, "正在运行")
                            time.sleep(2.5)
                        else:
                            break
            if int(conn.get(subdevice_key).decode()) and int(conn.get(transmit_key).decode()):
                # 传输程序跳出来后 再次判断设备和传输是否启动
                continue
            else:
                if int(conn.get(subdevice_key).decode()) == 0:
                    # 设备被禁用 陷入假循环
                    conn.set(status_key, "设备被禁用")
                    print(subdevice_id + transmit_id + "设备被禁用")
                    time.sleep(.5)
                    continue
                if int(conn.get(transmit_key).decode()) == 0:
                    # 传输通道关闭 程序终止
                    print(subdevice_id + transmit_id + "转发停止")
                    mqttclient.mqttc.loop_stop()
                    mqttclient.mqttc.disconnect()
                    break

        # print(transmit_ip)

