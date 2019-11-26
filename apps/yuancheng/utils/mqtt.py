import json
import time
import requests
from celery.task import Task
import django
django.setup()
from django_redis import get_redis_connection
from paho.mqtt.client import Client
import paho.mqtt.client as mqtt
from ctypes import *
import json
import time
from apps.shebei.models import SubDevice
from apps.yuancheng.models import GateWaySettingDown
from apps.loginfo.models import Log_list
import os

MQTTHOST = "10.129.7.199"
MQTTPORT = 1883
mqttClient = mqtt.Client()

GateWay = GateWaySettingDown.objects.values()

class mqtt_Sub():
    # def __init__(self):
    #     mqtt_Sub.get_data()

    def on_connect(self, client, userdata, flags, rc):
        print('on connect rc', rc)

    def on_connect1(self, client, userdata, flags, rc):
        print('on connect rc', rc)

    def on_message(self, client, userdata, msg):
        data = json.loads(msg.payload.decode('gbk'))
        status = list(data.keys())[0]
        subtopic = msg.topic
        if subtopic[-6:] == "create":
            if status == "create_params":
                print(status)
                SubDevice.objects.create(subdevice_type=data["create_params"][0]["subdevice_type"],
                                               subdevice_name=data["create_params"][0]["subdevice_name"],
                                               subdevice_position=data["create_params"][0]["subdevice_position"],
                                               subdevice_secret = data["create_params"][0]["subdevice_secret"],
                                               subdevice_model=data["create_params"][0]["subdevice_model"],
                                               subdevice_remark=data["create_params"][0]["subdevice_remark"])
                Log_list.objects.create(log_type="Systemlog", log_leader="admin", log_level='info', log_info= "%s新增设备%s"%(data["create_params"][0]["subdevice_position"],data["create_params"][0]["subdevice_name"]), log_no=1)

        elif subtopic[-6:] == "update":
            if status == "update_params":
                print(status)
                SubDevice.objects.filter(subdevice_name=data["update_params"][0]["subdevice_name"]).update(subdevice_type=data["update_params"][0]["subdevice_type"],
                                         subdevice_position=data["update_params"][0]["subdevice_position"],
                                         subdevice_secret=data["update_params"][0]["subdevice_secret"],
                                         subdevice_model=data["update_params"][0]["subdevice_model"],
                                         subdevice_remark=data["update_params"][0]["subdevice_remark"])
                Log_list.objects.create(log_type="Systemlog", log_leader="admin", log_level='info',
                                        log_info="设备%s信息更新完毕"%data["update_params"][0]["subdevice_name"], log_no=1)

        elif subtopic[-6:] == "delete":
            if status == "delete_params":
                print(status)
                SubDevice.objects.filter(subdevice_name=data["delete_params"][0]["subdevice_name"]).delete()
                Log_list.objects.create(log_type="Systemlog", log_leader="admin", log_level='info',
                                        log_info= "设备%s已删除"%data["delete_params"][0]["subdevice_name"] , log_no=1)

    def on_publish(self, client, userdata, mid):
        print('on publish mid', mid)

    def on_subscrib(self, client, userdata, mid, qos):
        print('on subscribe mid', mid)

    def on_disconnect(self, client, userdata, rc):
        print("disconnect reconnect later!")

    def cnct(self):
        print("连接MQTT...")
        #  5、整理得到的結果提取 username，password，port，host
        # try:
        username = "iot"
        password = "iot123!"
        port = 1883
        host = "10.129.7.199"
        self.mqttClient = Client(client_id="F1334780")
        self.mqttClient.on_connect = self.on_connect
        self.mqttClient.on_message = self.on_message
        self.mqttClient.on_publish = self.on_publish
        self.mqttClient.on_subscribe = self.on_subscrib
        self.mqttClient.on_disconnect = self.on_disconnect
        self.mqttClient.username_pw_set(username=username, password=password)
        self.mqttClient.connect(port=port, host=host, keepalive=90)
        self.mqttClient.loop_start()
        print("MQTT连接OK   ----")

    def get_data(self):
        self.cnct()
        for i in GateWay:
            self.mqttClient.subscribe(topic="%s"%i['down_topic'], qos=1)




# def ping(ID):
#     d = os.popen('ping %s'%ID)
#     f = d.read()
#     return (f)
# print(ping('10.129.5.55'))

def ping(action):
    d = os.popen(action)
    f = d.read()
    return (f)
