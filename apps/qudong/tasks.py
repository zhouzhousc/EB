#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/31 17:46
# @Author  : userzhang
import binascii
import json
import re
import time
from ctypes import *

import requests
import serial
from celery.task import Task
import django
from django_redis import get_redis_connection

django.setup()
from .utils.Crc import calculate_CRC


class Drive_modebusrtu(Task):
    name = "Drive_modebusrtu"

    def run(self, subdevice_id, info, cmd_dict):
        '''定义设备采集驱动drive 函数 '''
        print("start run modbus drive")
        self.info = info
        self.cmd_dict =cmd_dict
        self.subdevice_id =int(subdevice_id)
        self.key = "template_{}".format(self.subdevice_id)
        self.conn = get_redis_connection('default')



        # self.load = {}

        # 打开串口
        self.openser()

        print("end run modbus drive")
        return True

    def openser(self):
        time.sleep(5)
        # 等待上一个任务终止 清除占用资源
        self.conn.hset(self.key, "enable", 1)

        with serial.Serial(self.info[0], baudrate=int(self.info[2]), timeout=float(self.info[5])) as ser:
            if ser.isOpen():
                # while True
                print("串口打开成功")
                # enable = int(self.conn.hget(self.key, "enable").decode())
                while int(self.conn.hget(self.key, "enable").decode()):
                    self.collect(ser)
                    print(float(self.info[6])-0.5)
                    self.sleep(float(self.info[6])-0.5)
        print("串口关闭")


    def sleep(self, s):
        while s:
            if int(self.conn.hget(self.key, "enable").decode()):
                s = round(s - 0.1, 1)
                time.sleep(.1)
            else:
                break

    def collect(self, ser):
        data = self.init(ser)
        json_str = json.dumps(data)
        print(json_str)
        # 往api 里 写数据
        # 3. 写入设备API
        proxies = {"http": "", "https": "", }  # 不使用系统全局代理
        headers = {'Connection': 'close'}  # 在短时间使用多次requests.get
        with requests.Session() as s:
            s.keep_alive = False
            data = s.post(url="http://127.0.0.1:9090/apidata/all",
                                 data={
                                     'data_status': 0,
                                     'data': json_str,
                                     'subdevice_id': self.subdevice_id,
                                     'data_type': 0},
                                 proxies=proxies,
                                 headers=headers
                                 )
        print(data)
        # data.close()

    def init(self, ser):
        load = {}
        for param, cmd in self.cmd_dict.items():
            cmd_crc = calculate_CRC(cmd[0])
            b_cmd_crc = binascii.a2b_hex(cmd_crc)
            # write 写入指令
            # return data
            ser.write(b_cmd_crc)
            data = binascii.b2a_hex(ser.readall())
            rx = data.decode()
            if cmd[1] == 0:
                load[param] = rx[6:-4]
            elif cmd[1] == 1:
                a = cmd[2]
                b = str(int(rx[6:-4], 16))
                if re.match(r"[-+*/]",a):
                    load[param] = str(eval(b+a))
                else:
                    load[param] = b
            elif cmd[1] == 2:
                load[param] = str(self.convert(rx[6:-4]))

        return load

    def convert(self, s):
        ''' IEEE 格式化 '''
        try:
            i = int(s, 16)  # convert from hex to a Python int
            cp = pointer(c_int(i))  # make this into a c integer
            fp = cast(cp, POINTER(c_float))  # cast the int pointer to a float pointer
            return fp.contents.value  # dereference the pointer, get the float
        except:
            return "NA"

