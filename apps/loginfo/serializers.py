#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/8 17:05 
# @Author  : zhuyuanbo


from rest_framework import serializers
from .models import Event_list, NoticeManager, Log_list,Name


class Event_listSerializers(serializers.ModelSerializer):
    class Meta:
        model = Event_list  # 指定的模型类
        fields = ('pk', 'event_no', 'event_leader', 'event_info', 'event_create_time', 'event_type')  # 需要序列化的属性

class NoticeManagerSerializers(serializers.ModelSerializer):
    notice_status = serializers.BooleanField()
    notice_message_num = serializers.IntegerField()
    class Meta:
        model = NoticeManager  # 指定的模型类
        fields = ('id', 'notice_leader','is_delete','notice_location', 'notice_message_num', 'notice_time', 'notice_status', 'notice_phone', 'notice_email')  # 需要序列化的属性

class Log_listSerializers(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Log_list  # 指定的模型类
        fields = ('id', 'create_time', 'log_type', 'log_leader', 'log_level', 'log_info', 'log_no')  # 需要序列化的属性

# class NameSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Name  # 指定的模型类
#         fields = ('name', 'age', 'create_time')  # 需要序列化的属性
