# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # @Time    : 2019/5/22 10:15
# # @Author  : zhuyuanbo

import json
import time
import psutil
import os, datetime
import pymysql
import datetime
import sys
import netifaces
import serial.tools.list_ports
import socket
sys.coinit_flags = 0
import pythoncom
import wmi
import serial.tools.list_ports


class systemos:
    def __init__(self):
        self.integrated = {}
        self.GetCpuInfo()
        self.GetDiskInfo()
        self.datatime()

    # 获取CPU信息
    def GetCpuInfo(self):
        cpu_slv = round((psutil.cpu_percent(1)), 2)  # cpu使用率
        memory = psutil.virtual_memory()
        total_nc = round((float(memory.total) / 1024 / 1024 / 1024), 2)  # 总内存
        free_nc = round((float(memory.free) / 1024 / 1024 / 1024), 2)  # 空闲内存
        routingGateway = netifaces.gateways()['default'][netifaces.AF_INET][0]
        routingNicName = netifaces.gateways()['default'][netifaces.AF_INET][1]
        for interface in netifaces.interfaces():
            if interface == routingNicName:
                routingIPNetmask = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['netmask']
        self.integrated['sys_gateway'] = routingGateway
        self.integrated['sys_mask'] = routingIPNetmask
        self.integrated['sys_rateof_cpu'] = cpu_slv
        self.integrated['sys_memory'] = total_nc
        self.integrated['sys_memory_size'] = round(int(free_nc) / int(round(total_nc)),3) * 100

    def GetDiskInfo(self):
        list = psutil.disk_partitions()[0:4]  # 磁盘列表
        ilen = len(list)  # 磁盘分区个数
        i = 0
        retlist1 = []
        retlist2 = []
        while i < ilen:
            diskinfo = psutil.disk_usage(list[i].device)
            total_disk = round((float(diskinfo.total) / 1024 / 1024 / 1024), 2)  # 总大小
            used_disk = round((float(diskinfo.used) / 1024 / 1024 / 1024), 2)  # 已用大小
            free_disk = round((float(diskinfo.free) / 1024 / 1024 / 1024), 2)  # 剩余大小
            syl_disk = diskinfo.percent

            retlist1 = [i, list[i].device, total_disk, used_disk, free_disk, syl_disk]  # 序号，磁盘名称，
            retlist2.append(retlist1)
            i = i + 1
        memory = 0
        usermemory = 0
        for i in retlist2:
            memory += i[2]
            usermemory += i[3]
        self.integrated['sys_harddisk'] =  round((int(usermemory) / int(memory)) * 100 ,1)
        self.integrated['sys_harddisk_size'] = round((round(memory,2)),3)

    def datatime(self):
        time_now = int(time.time())
        time_local = time.localtime(time_now)
        currenttime = time.strftime("%Y-%m-%d %H:%M:%S", time_local)

        dt = datetime.datetime.fromtimestamp(psutil.boot_time())
        starttime = dt.strftime("%Y-%m-%d,%H:%M:%S")
        starttime = starttime.replace(',', ' ')

        currenttime = datetime.datetime.strptime(currenttime, "%Y-%m-%d %H:%M:%S")
        starttime = datetime.datetime.strptime(starttime, "%Y-%m-%d %H:%M:%S")
        timename = currenttime - starttime  # 运行时间
        self.integrated['sys_running_time'] = timename
        self.integrated['sys_local_time'] = currenttime


    # 启动时间
    def Getsystem(self):
        pythoncom.CoInitialize()
        c = wmi.WMI()
        for interface in c.Win32_NetworkAdapterConfiguration(IPEnabled=1):
            MAC = interface.MACAddress
        myname = socket.getfqdn(socket.gethostname())
        myaddr = socket.gethostbyname(myname)
        # ip_add1 = ip_address
        # # 系统信息:系统版本,主机名,系统安装时间,系统位数,串口ID,总内存大小
        system = ['Caption', 'CSName', 'InstallDate', 'OSArchitecture', 'SerialNumber', 'TotalVisibleMemorySize']
        system_msg = list()

        for sys in c.Win32_OperatingSystem():
            for i in system:
                if i == 'InstallDate':
                    system_msg.append(getattr(sys, i).split('.')[0])
                elif i == 'TotalVisibleMemorySize':
                    system_msg.append("%sGB" % round(int(getattr(sys, i)) / (1024 * 1024)))
                else:
                    system_msg.append(getattr(sys, i))

        ser = list()
        port_list = list(serial.tools.list_ports.comports())
        for i in port_list:
            if i[0] != 'COM1' and i[0] != 'COM2':
                ser.append(i[0])
                ser = ser[0]

        if ser == []:
            ser = 0

        # self.integrated['sys_com'] = 0
        self.integrated['sys_mac'] = MAC
        self.integrated['sys_ip'] = myaddr
        name = (dict(zip(system, system_msg)))
        self.integrated['sys_os'] = name['Caption']
        self.integrated['sys_hostname'] = name['CSName']
        self.integrated['sys_out_time'] =  '2019-10-25'
        self.integrated['is_delete'] = 1
        self.integrated['sys_product_name'] = 'Gateway'
        self.integrated['sys_net_status'] = 1
        self.integrated['sys_use_usb_num'] = int(len(list(serial.tools.list_ports.comports())))
        self.integrated['sys_usb_num'] = 4
        self.integrated['sys_com'] = ser


        self.integrated['sys_rs232_num'] = 2
        self.integrated['sys_net_model'] = 'MQTT请求'
        return self.integrated
        pythoncom.CoUninitialize()


def main(database):
    now_time = datetime.datetime.now()
    parameters = systemos().Getsystem()
    database.objects.filter(id=1).update(is_delete=parameters['is_delete'],sys_hostname=parameters['sys_hostname'],sys_product_name=parameters['sys_product_name'], sys_os=parameters['sys_os'],sys_ip=parameters['sys_ip'],
    sys_mac=parameters['sys_mac'], sys_mask=parameters['sys_mask'],sys_gateway=parameters['sys_gateway'], sys_net_status=parameters['sys_net_status'],
    sys_rateof_cpu=parameters['sys_rateof_cpu'],sys_memory=parameters['sys_memory'], sys_memory_size=parameters['sys_memory_size'],sys_harddisk=parameters['sys_harddisk'],
    sys_harddisk_size=parameters['sys_harddisk_size'], sys_usb_num=parameters['sys_usb_num'], sys_rs232_num=parameters['sys_rs232_num'], sys_running_time=parameters['sys_running_time'],
    sys_local_time=parameters['sys_local_time'],sys_out_time=parameters['sys_out_time'], sys_net_model=parameters['sys_net_model'],sys_use_usb_num=parameters['sys_use_usb_num'],sys_com=parameters['sys_com'])
    print('写入成功')
    end_time = datetime.datetime.now()
    time = end_time - now_time
    print(time)


def message():
    parameters = systemos().Getsystem()
    return parameters



# print(message())
#
#
# def name():
#     parameters = systemos().Getsystem()
#     return (parameters)
#
# print(name())

# from psutil import net_if_addrs
#
# for k, v in net_if_addrs().items():
#     for item in v:
#         address = item[1]
#         if '-' in address and len(address) == 17:
#             print(address)