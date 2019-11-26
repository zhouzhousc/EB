#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/12 14:30 
# @Author  : zhuyuanbo


from rest_framework import serializers
from .models import SysInfo


class SysInfoSerializers(serializers.ModelSerializer):
    sys_local_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    sys_out_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model = SysInfo  # 指定的模型类
        fields = ('sys_hostname', 'sys_product_name', 'sys_os', 'sys_ip', 'sys_mac', 'sys_mask', 'sys_gateway', 'sys_net_status',
                  'sys_harddisk_size', 'sys_rateof_cpu', 'sys_memory', 'sys_memory_size', 'sys_harddisk', 'sys_usb_num', 'sys_rs232_num',
                  'sys_running_time', 'sys_local_time', 'sys_out_time', 'sys_net_model',"sys_use_usb_num","sys_com")  # 需要序列化的属性