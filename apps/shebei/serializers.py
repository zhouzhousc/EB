#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/12 19:57
# @Author  : userzhang
from rest_framework import serializers
# from apps.apidata.models import CollectData, M5Data
from apps.shebei.models import DataTransmitList
# from apidata.models import CollectData


class DataTransmitListSerializer(serializers.ModelSerializer):

    # subdevice_id =serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # subdevice_id = SubDeviceSerializer()
    #自定义字段
    subdevice_id = serializers.SerializerMethodField()
    class Meta:
        model = DataTransmitList
        # 和"__all__"等价
        # fields = ("id",'subdevice_id', 'transmit_type', 'transmit_status', 'transmit_name',
        #           'transmit_remark','create_time','transmit_ip',"transmit_port",'')
        fields = '__all__'

    #自定义字段获取关联字段
    def get_subdevice_id(self, obj):
        return obj.subdevice.id

    #创建
    def create(self, validated_data):
        # 处理外键字段
        return DataTransmitList.objects.create(subdevice=self.context["subdevice"], **validated_data)

