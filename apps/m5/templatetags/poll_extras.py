#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/2 16:20
# @Author  : userzhang
from django import template

register = template.Library()
from django_redis import get_redis_connection

# 组成列表
@register.filter(name='tolist')
def tolist(str1, str2):
    return [str1, str2]


# 选取最大值
@register.filter(name='maxus')
def maxus(m5device, value):
    try:
        print(m5device)
        value = int(value)
        conn = get_redis_connection('default')
        m5_params = "m5paramsmax_{}".format(m5device[0])
        b_v=conn.hget(m5_params, m5device[1])
        if b_v is None:
            conn.hset(m5_params, m5device[1], value)
            return value
        if value >= int(b_v.decode()):
            conn.hset(m5_params, m5device[1], value)
            return value
        return b_v.decode()


    except Exception as e:
        print("error:",e)
        value = "null"
        return value

# 选取最大值
@register.filter(name='mixus')
def mixus(m5device, value):
    try:
        print(m5device)
        value = int(value)
        conn = get_redis_connection('default')
        m5_params = "m5paramsmix_{}".format(m5device[0])
        b_v = conn.hget(m5_params, m5device[1])
        if b_v is None:
            conn.hset(m5_params, m5device[1], value)
            return value
        if value <= int(b_v.decode()):
            conn.hset(m5_params, m5device[1], value)
            return value
        return b_v.decode()

    except Exception as e:
        print("error:",e)
        value = "null"
        return value


# 选取最大值
@register.filter(name='averagenumus')
def averagenumus(m5device, value):
    try:
        print(m5device)
        value = int(value)
        conn = get_redis_connection('default')
        m5_paramsavg = "m5paramsavg_{}_{}".format(m5device[0], m5device[1])
        conn.lpush(m5_paramsavg, value)
        l=conn.lrange(m5_paramsavg, 0, 10)
        # print(l)
        nsum=0
        for n in range(len(l)):
            nsum += int(l[n].decode())
        return round(nsum / len(l), 3)

    except Exception as e:
        print("error:",e)
        value = "null"
        return value