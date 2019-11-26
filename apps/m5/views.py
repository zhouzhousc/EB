import json

from django.shortcuts import render
from django.views.generic import View
from django.forms.models import model_to_dict
# Create your views here.t
from random import randint
from django_redis import get_redis_connection
from apps.apidata.models import M5Data
# /m5/manage
class M5ManageView(View):
    '''网关管理'''
    def get(self, request):
        m5_devices=[]
        conn = get_redis_connection('default')
        m5 = "m5_*"
        devices = conn.keys(m5)
        for m5 in devices:
            b_info=conn.hgetall(m5.decode())
            info={}
            for i,value in b_info.items():
                key = i.decode()
                info[key]=value.decode()
                if key == "m5device_name":
                    info[key]="m5_"+info[key]
            m5_devices.append(info)
        print(m5_devices)
        # m5_devices["m5device_name"] = "m5_"+m5_devices["m5device_name"]
        # context = {
        #     "m5_devices": m5_devices
        # }

        return render(request, 'm5/M5_Pair_Connection.html', locals() )

# /m5/manage/<device_id>
class M5DeviceManageView(View):
    '''M5设备的管理主页面'''
    def get(self, request, m5device_name):
        conn = get_redis_connection('default')
        # m5="m5_%s" % m5device_name
        b_info = conn.hgetall(m5device_name)
        info = {}
        for i, value in b_info.items():
            key = i.decode()
            info[key] = value.decode()
            if key == "m5device_name":
                info[key] = "m5_" + info[key]
        print(info)
        context = {
            "info": info
        }
        return render(request, 'm5/M5_Docking_Module_Main.html', context)


# TODO(Jianli) /m5/manage/devicedebug/<device_id>

class M5DeviceDebugView(View):
    '''M5设备的特征提取页面'''
    def get(self, request, m5device_name):
        print(m5device_name)
        data=M5Data.objects.filter(subdevice_name=m5device_name).order_by("-id")[0]
        data=json.loads(data.data)
        # data=data["m5device_forward"][0]
        print(data)
        return render(request, 'm5/Feature_Extraction.html', locals())


# /m5/manage/devicedataforward/<device_id>
class M5DeviceDataView(View):
    '''M5设备的数据转发页面'''

    def get(self, request, m5device_name):
        m5paths = []
        conn = get_redis_connection('default')
        m5path_key = "m5path_%s_*" % m5device_name.split("_")[1]
        b_paths = conn.keys(m5path_key)
        for path in b_paths:
            b_info = conn.hgetall(path.decode())
            info = {}
            for i, value in b_info.items():
                info[i.decode()] = value.decode()
            m5paths.append(info)
        context = {
            "m5paths": m5paths
        }
        print(m5paths)
        return render(request, 'm5/Data_Forwarding.html', context)
