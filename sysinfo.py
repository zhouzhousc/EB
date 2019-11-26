# # #!/usr/bin/env python
# # # -*- coding: utf-8 -*-
# # # @Time    : 2019/5/22 10:15
# # # @Author  : zhuyuanbo
#
import wmi
import json
import time
import psutil
import os, datetime
import pymysql
import datetime
import sys
import netifaces


class systemos:
    sys_hostname=""         #系统主机名
    sys_product_name=""     #产品名
    sys_os=""               #系统操作环境
    sys_ip=""               #系统ip地址
    sys_mac=""              #系统mac地址
    sys_gateway=""          #系统默认网关
    sys_net_status=""       #系统网路状态
    sys_rateof_cpu=""       #系统CPU使用率
    sys_memory=""           #系统剩余内存 %
    sys_memory_size=""      #系统内存总量
    sys_harddisk=""         #系统硬盘剩余大小 %
    sys_harddisk_size=""    #系统硬盘总量
    sys_usb_number=""       #系统USB接口数
    sys_rs232_number=""     #系统Rs232接口数
    sys_running_time=""     #系统运行时间
    sys_local_time=""       #系统本地时间
    sys_out_time=""         #系统出厂日期
    sys_net_model=""        #系统网络模块

    def __init__(self):
        self.GetMemoryInfo()
        self.GetDiskInfo()
        self.sys_local_time()
        self.datatime()

    # 获取CPU信息
    def GetCpuInfo(self):
        # cpu使用率
        self.sys_rateof_cpu=  round((psutil.cpu_percent(1)), 2)

    # 获取内存信息
    def GetMemoryInfo(self):
        memory = psutil.virtual_memory()
        total_nc = round((float(memory.total) / 1024 / 1024 / 1024), 2)  # 总内存
        used_nc = round((float(memory.used) / 1024 / 1024 / 1024), 2)  # 已用内存
        free_nc = round((float(memory.free) / 1024 / 1024 / 1024), 2)  # 空闲内存
        syl_nc = round((float(memory.free) / float(memory.total) * 100), 2)  # 内存剩余百分比使用率
        # routingGateway = netifaces.gateways()['default'][netifaces.AF_INET][0]
        # routingNicName = netifaces.gateways()['default'][netifaces.AF_INET][1]
        #
        # for interface in netifaces.interfaces():
        #     if interface == routingNicName:
        #         routingIPNetmask = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['netmask']
        # self.integrated['sys_gateway'] = routingGateway
        # self.integrated['sys_mask'] = routingIPNetmask
        self.sys_memory = free_nc+syl_nc
        self.sys_memory_size = total_nc

    # 获取硬盘信息
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

        return retlist2
        # memory = 0
        # usermemory = 0
        # for i in retlist2:
        #     memory += i[2]
        #     usermemory += i[3]
        # self.integrated['sys_harddisk'] = usermemory
        # self.integrated['sys_harddisk_size'] = memory

    def Networkcard(self):
        routingGateway = netifaces.gateways()['default'][netifaces.AF_INET][0]
        routingNicName = netifaces.gateways()['default'][netifaces.AF_INET][1]

        for interface in netifaces.interfaces():
            if interface == routingNicName:
                routingNicMacAddr = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
                try:
                    routingIPAddr = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
                    routingIPNetmask = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['netmask']
                except KeyError:
                    pass
        self.sys_gateway = routingGateway
        self.sys_mask = routingIPNetmask
        # return self.integrated

    def datatime(self):
        time_now = int(time.time())
        time_local = time.localtime(time_now)
        dtime = time.strftime("%Y-%m-%d %H:%M:%S", time_local)

        dt = datetime.datetime.fromtimestamp(psutil.boot_time())
        starttime = dt.strftime("%Y-%m-%d,%H:%M:%S")
        starttime = starttime.replace(',', ' ')

        currenttime = dtime
        currenttime = datetime.datetime.strptime(currenttime, "%Y-%m-%d %H:%M:%S")
        starttime = datetime.datetime.strptime(starttime, "%Y-%m-%d %H:%M:%S")
        timename = currenttime - starttime  # 运行时间
        self.integrated['sys_running_time'] = timename

    def sys_local_time(self):
        time_now = int(time.time())
        time_local = time.localtime(time_now)
        dtime = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        self.integrated['sys_out_time'] = dtime
        self.integrated['sys_local_time'] = dtime

    # 启动时间
    def Getsystem(self):
        message = []
        c = wmi.WMI()
        msg = {}
        for interface in c.Win32_NetworkAdapterConfiguration(IPEnabled=1):
            MAC = interface.MACAddress
        # for ip_address in interface.IPAddress:
        ip_add = interface.IPAddress[0]

        # ip_add1 = ip_address
        # # 系统信息:系统版本,主机名,系统安装时间,系统位数,串口ID,总内存大小
        # system = ['Caption', 'CSName', 'InstallDate', 'OSArchitecture', 'SerialNumber', 'TotalVisibleMemorySize']
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
        cpu = ['Name']
        cpu_msg = []
        name = {}
        for i in c.Win32_Processor():
            for i2 in cpu:
                cpu_msg.append(getattr(i, i2))
        msg['CPU'] = dict(zip(cpu, cpu_msg))
        # self.integrated['CPU'] = msg['CPU']['Name'][:22] + msg['CPU']['Name'][-16:-8] + msg['CPU']['Name'][-7:]
        self.integrated['sys_mac'] = MAC
        self.integrated['sys_ip'] = ip_add
        # self.integrated.append(msg)
        name = (dict(zip(system, system_msg)))
        self.integrated['sys_os'] = name['Caption']
        self.integrated['sys_hostname'] = name['CSName']
        self.integrated['create_time'] =  '2018-10-12'
        self.integrated['update_time'] = '2019-05-05'
        self.integrated['is_delete'] = 1
        self.integrated['sys_product_name'] = 'Gateway'
        self.integrated['sys_net_status'] = '在线'
        self.integrated['sys_usb_num'] = 4
        self.integrated['sys_rs232_num'] = 2
        self.integrated['sys_net_model'] = 'MQTT请求'

        return self.integrated


def message():
    parameters = systemos().Getsystem()
    print((parameters))


if __name__ == '__main__':
    message()


# import socket
# myname = socket.getfqdn(socket.gethostname())#获取本机ip
# myaddr = socket.gethostbyname(myname)
# print (myname.split(".")[0],myaddr)

# a = []
# from psutil import net_if_addrs
# for k, v in net_if_addrs().items():
#     for item in v:
#         address = item[1]
#         if '-' in address and len(address) == 17:
#                 a.append(address)
# print(a)
