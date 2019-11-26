import json
import time
import requests
from celery.task import Task
import django
import paho.mqtt.subscribe as subscribe
from paho.mqtt.client import Client
django.setup()
from django_redis import get_redis_connection
# from .Core.auth_corepro import AuthCorepro
# from .Core.mqtt_pub_sub import mqtt_client_connect


from apps.shebei.models import SubDevice

class mqtt_Sub(Task):

    def on_connect(self, client, userdata, flags, rc):
        print('on connect rc', rc)

    def on_connect1(self, client, userdata, flags, rc):
        print('on connect rc', rc)

    def on_message(self, client, userdata, msg):
        device = eval(str(msg.payload)[2:-1])
        print(device)
        sub = SubDevice.objects.create(subdevice_name=device["create_params"][0]["subdevice_name"],
                                     subdevice_type=device["create_params"][0]["subdevice_type"],
                                     subdevice_position=device["create_params"][0]["subdevice_position"],
                                     subdevice_model=device["create_params"][0]["subdevice_model"],
                                     subdevice_remark=device["create_params"][0]["subdevice_remark"])
        sub.save()

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
        self.mqttClient = Client(client_id="F1334790")
        self.mqttClient.on_connect = self.on_connect
        self.mqttClient.on_message = self.on_message
        self.mqttClient.on_publish = self.on_publish
        self.mqttClient.on_subscribe = self.on_subscrib
        self.mqttClient.on_disconnect = self.on_disconnect
        self.mqttClient.username_pw_set(username=username, password=password)
        self.mqttClient.connect(port=port, host=host, keepalive=90)
        self.mqttClient.loop_start()
        print("MQTT连接OK   ----")
        # except Exception as e:
        #     print("MQTT连接异常：", e)

        # time.sleep(3)

    def get_data(self):
        self.cnct()
        self.mqttClient.subscribe(topic="/data/EdgeBox/gateway/create", qos=1)
        # while True:
        #     pass

