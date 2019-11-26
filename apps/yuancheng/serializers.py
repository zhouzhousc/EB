#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/8 17:05 
# @Author  : zhuyuanbo


from rest_framework import serializers
from .models import GateWaySettingDown


class Setting_down(serializers.ModelSerializer):
    class Meta:
        model = GateWaySettingDown  # 指定的模型类
        fields = ('down_type', 'down_topic', 'down_remark', 'down_num')  # 需要序列化的属性