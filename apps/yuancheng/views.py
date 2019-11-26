from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from .serializers import Setting_down
from .models import GateWaySettingDown
from apps.wangguang.models import RegisterInfo
from rest_framework import viewsets, filters, pagination
from yuancheng.utils.mqtt import mqtt_Sub,ping
from apps.loginfo.models import Log_list
from django.core import serializers
import json
# Create your views here.

# loginfo/manage
class YuanchengManageView(View):
    '''日志管理'''
    def get(self, request):

        return render(request, 'yuancheng/Remote_Manage_Main.html' )


class YuanchengConfigView(View):
    '''日志中心'''

    def get(self, request):
        return render(request, 'yuancheng/Configuration_Distribution.html')


class YuanchengRemoteView(View):
    '''事件中心'''

    def get(self, request):
        return render(request, 'yuancheng/Remote_Manage.html')



class GateWaySetting(viewsets.ModelViewSet):
    # 指定结果集并设置排序
    queryset = GateWaySettingDown.objects.all().order_by('-pk')
    serializer_class = Setting_down
    mqtt_Sub().get_data()
    def get_queryset(self):
        queryset = GateWaySettingDown.objects.values()
        wangguang_name = RegisterInfo.objects.values("gateway_name")
        for i in queryset:
            i['down_topic'] = "data/%s/%s" % ((wangguang_name[0]['gateway_name']),i['down_type'])
            queryset = GateWaySettingDown.objects.filter(down_type=i['down_type']).update(down_topic=i['down_topic'])

        queryset = GateWaySettingDown.objects.filter()

        return queryset


def get_log(request):
    '''

    :param request:
    :return:
    '''
    # if request.method == "GET":
    #     ip = request.GET.get("ip")
    #     if ip:
    #         print("success")
    #         print(ip)
    #         json_db =ping(ip)
    #         print(json_db)
    #
    #         return JsonResponse({
    #             # json_db
    #             "status_code": 0,
    #             "db": json_db
    #         })
    if request.method == "GET":
        action = request.GET.get("action")
        if action[:4] == 'ping' or action == 'ipconfig' or action == 'ipconfig /all':
            cmd_return = ping(action).replace("\n", "&")
            if action[:4] == 'ping':
                Log_list.objects.create(log_type="Weblog", log_leader="admin", log_level='info',
                                        log_info="%s成功"%action, log_no=1)
            print(action)
            return JsonResponse({
                # json_db
                "status_code": 0,
                "db": cmd_return
            })
        # def ping(ID):
        #     d = os.popen('ping %s' % ID)
        #     f = d.read()
        #     return (f)
        # # print(ping('10.129.5.55'))

    if request.method == "POST":
       pass
