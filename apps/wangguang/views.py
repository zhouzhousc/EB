from django.shortcuts import render
from django.views.generic import View
# from wangguang.models import RegisterInfo, SysInfo
from apps.wangguang.models import RegisterInfo, SysInfo
import datetime, requests
from rest_framework import viewsets, filters, pagination
from .serializers import SysInfoSerializers
from apps.wangguang.utils.systemos import message,main
from rest_framework.decorators import api_view
from django.http import HttpResponse,JsonResponse

# Create your views here.

# app_name = 'apps.wangguang'
# /gateway/manage
class GatewayManageView(View):
    '''网关管理'''
    def get(self, request):

        data = RegisterInfo.objects.all().order_by('-id')[0]
        context = {
            "data": data
        }
        # session = requests.Session()
        # session.trust_env = False
        # data = session.get(url="http://127.0.0.1:9090/apidata/all")
        # print(data.json())
        return render(request, 'wangguang/Gateway_Main.html' , context)

    def post(self, request):
        gateway_name=request.POST.get("gateway_name")
        gateway_id=request.POST.get("gateway_id")
        gateway_secret=request.POST.get("gateway_secret")
        gateway_authurl=request.POST.get("gateway_authurl")
        gateway_location=request.POST.get("gateway_location")
        gateway_remark=request.POST.get("gateway_remark")
        # print(gateway_name,gateway_location,gateway_remark,gateway_id,gateway_secret)
        data=RegisterInfo.objects.all().order_by('-id')[0]
        data.gateway_name=gateway_name
        data.gateway_id=gateway_id
        data.gateway_secret=gateway_secret
        data.gateway_authurl=gateway_authurl
        data.gateway_location=gateway_location
        data.gateway_remark=gateway_remark
        data.save()
        context = {
            "data": data
        }
        return render(request, 'wangguang/Gateway_Main.html', context)

# /gateway/info
class GatewayInfoView(View):
    '''网关基本信息'''
    def get(self, request):
        data=RegisterInfo.objects.all().order_by('-id')[0]
        context={
            "data": data
        }

        return render(request, 'wangguang/Gateway_Information.html', context)

# /gateway/sysinfo
class GatewaySysInfoView(View):
    '''网关系统信息'''
    def get(self, request):
        data = SysInfo.objects.all().order_by('-id')[0]
        context = {
            "data": data
        }

        return render(request, 'wangguang/System_Information.html', context)

# /gateway/service
class GatewayServiceView(View):
    '''网关基本信息'''
    def get(self, request):
        return render(request, 'wangguang/Initiated_Service.html')


class PageSet(pagination.PageNumberPagination):
    # 页面大小
    page_size = 10
    page_size_query_param = "size"
    max_page_size = 10
    page_query_param = "page"

class SysInfoViewSet(viewsets.ModelViewSet):
    # 指定结果集并设置排序
    queryset = SysInfo.objects.all().order_by('-pk')
    serializer_class = SysInfoSerializers
    pagination_class = PageSet
    # 配置搜索功能
    filter_backends = (filters.SearchFilter,)
    # 设置搜索的关键字
    search_fields = ('=sys_hostname', 'sys_product_name')
    # 设置搜索出的结果中需要排序的字段
    ordering_field = ('sys_hostname', 'sys_product_name')




@api_view(['GET', 'POST'])
def getlispic(request, format=None,):
    if request.method == "GET":
        now_time = datetime.datetime.now()
        type = request.GET.get("type")
        # try:
        # if type:
        main(SysInfo)
        # except Exception as e:
        #     print(e)
        db = SysInfo.objects.filter().order_by("id")
        obj = PageSet()
        page_list = obj.paginate_queryset(db, request)
        ser = SysInfoSerializers(instance=page_list, many=True)
        response = obj.get_paginated_response(ser.data)
        end_time = datetime.datetime.now()
        time = end_time - now_time
        print(time)
        return response

        # start_time = request.GET.get("start_time")
        # end_time = request.GET.get("end_time")
        # print(type, start_time, end_time)
        # if not type:
        #
        # else:
        # if type == 1:

        # if not all([start_time, end_time]):
        #     db = Log_list.objects.filter(log_no=type).order_by("id")
        #     obj = PageSet()
        #     page_list = obj.paginate_queryset(db, request)
        #     ser = Log_listSerializers(instance=page_list, many=True)
        #     response = obj.get_paginated_response(ser.data)
        #     return response
        # else:
        #     db = Log_list.objects.filter(log_no=type, create_time__gt=start_time,
        #                                  create_time__lt=end_time).order_by("id")
        #     obj = PageSet()
        #     page_list = obj.paginate_queryset(db, request)
        #     ser = Log_listSerializers(instance=page_list, many=True)
        #     response = obj.get_paginated_response(ser.data)
        #     return response

    if request.method == "POST":
       pass
