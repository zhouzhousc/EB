import json

from django.shortcuts import render
from django.views.generic import View
from apps.loginfo.models import Event_list, NoticeManager, Log_list,Name
import time
from django.http import JsonResponse
from .tasks import Send_enent_email_tasks
# from yuancheng.tasks import mqtt_Sub
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import viewsets
from django.core import serializers
from rest_framework.decorators import api_view
from .models import Event_list,Name
from .serializers import Event_listSerializers, NoticeManagerSerializers, Log_listSerializers
from rest_framework import viewsets, filters, pagination
from django.http import HttpResponse,JsonResponse
from django.db.models import Q
from rest_framework.pagination import LimitOffsetPagination
# Create your views here.


def datatime():
    time_now = int(time.time())
    time_local = time.localtime(time_now)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return dt


# loginfo/manage
class LoginfoManageView(View):
    '''日志管理'''

    def get(self, request):
        # NoticeView = NoticeManager.objects.filter(id=10)[0]
        #
        # # print(NoticeView1)
        # Messagedata = {
        #     "NoticeView": NoticeView
        # }

        return render(request, 'loginfo/Logging_Events_Main.html')

    def post(self, request):
        '''post请求添加一条路径记录'''
        # all = request.POST
        # print(all)
        person_liable = request.POST.get("person_liable")
        mobile_phone = request.POST.get("mobile_phone")
        mailbox = request.POST.get("mailbox")
        position = request.POST.get("position")

        notice = NoticeManager.objects.create(notice_leader=person_liable,
                                              notice_location=position,
                                              notice_phone=mobile_phone,
                                              notice_message_num=6,
                                              notice_time=datatime(),
                                              notice_email=mailbox)
        notice.save()

        NoticeView = NoticeManager.objects.all()
        Messagedata = {
            "NoticeView": NoticeView,
        }
        # return render(request, 'loginfo/Notification_Management.html', Messagedata)
        return render(request, 'loginfo/Logging_Events_Main.html')


class LoginfoLoggerView(View):
    '''日志中心'''

    def get(self, request):
        infos = Log_list.objects.all()
        #數據拿出來
        content={
            "infos":infos,

        }
        return render(request, 'loginfo/log_Center.html',content)


class LoginfoEventView(View):
    '''事件中心'''

    def get(self, request):
        return HttpResponse(u'欢迎光临 Django!')
        # EventView = Event_list.objects.all()
        # EventViewMessagedata = {
        #     "EventView": EventView,
        # }
        # return render(request, 'loginfo/Event_Center.html', EventViewMessagedata)

# loginfo/notice/delete
class NoticeManageDeleteApi(View):
    '''刪除通知人的api'''
    def post(self, request):
        id=request.POST.get("id")
        print(id)
        notice=NoticeManager.objects.get(id=int(id))
        notice.delete()
        # 檢驗數據
        # 業務處理
        # 返回成功
        return JsonResponse({'res': 3, 'message': '删除成功'})



class LoginfoNoticeView(View):
    '''通知管理'''

    def get(self, request):
        # 數據拿出來
        # details = request.POST.get("details")
        NoticeView = NoticeManager.objects.all().order_by('-id')

        Messagedata = {
            "NoticeView": NoticeView,
        }

        return render(request, 'loginfo/Notification_Management.html', Messagedata)

    def post(self, request):
        NoticeView = NoticeManager.objects.all().order_by('-id')
        Messagedata = {
            "NoticeView": NoticeView,
        }

        return render(request, 'loginfo/Notification_Management.html', Messagedata)


class PageSet(pagination.PageNumberPagination):
    # 页面大小
    # page_size = 2
    page_size_query_param = "size"
    # max_page_spaginate_querysetize = 1
    page_query_param = "page"

# class StandardResultSetPagination(LimitOffsetPagination):
#     # 默认每页显示的条数
#     default_limit = 20
#     # url 中传入的显示数据条数的参数
#     limit_query_param = 'limit'
#     # url中传入的数据位置的参数
#     offset_query_param = 'offset'
#     # 最大每页显示条数
#     max_limit = None

class EventViewSet(viewsets.ModelViewSet):
    # 指定结果集并设置排序
    queryset = Event_list.objects.all().order_by("id")
    Send_enent_email_tasks.delay()

    serializer_class = Event_listSerializers
    pagination_class = PageSet
    # # 配置搜索功能
    # filter_backends = (filters.SearchFilter,)
    # # 设置搜索的关键字
    # search_fields = ('=event_leader', 'event_info')
    # # 设置搜索出的结果中需要排序的字段
    # ordering_field = ('event_leader', 'event_info')
    def get_queryset(self):
        queryset = Event_list.objects.all()
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(Q(event_leader__icontains=search) | Q(event_info__icontains=search) |Q(event_create_time__icontains=search) |
            Q(event_type__icontains=search) | Q(event_no__icontains=search))

        return queryset


class NoticeManagerViewSet(viewsets.ModelViewSet):
    # 指定结果集并设置排序
    queryset = NoticeManager.objects.all().order_by('-pk')
    serializer_class = NoticeManagerSerializers
    pagination_class = PageSet
    # # 配置搜索功能
    # filter_backends = (filters.SearchFilter,)
    # # 设置搜索的关键字
    # search_fields = ('=notice_leader', 'notice_phone')
    # # 设置搜索出的结果中需要排序的字段
    # ordering_field = ('notice_leader', 'notice_phone')
    def get_queryset(self):
        queryset = NoticeManager.objects.filter(is_delete=0)
        search = self.request.query_params.get('search')
        delete = self.request.query_params.get('delete')
        id = self.request.query_params.get('id')
        status = self.request.query_params.get('status')
        if search:
            queryset = queryset.filter(Q(notice_leader__icontains=search) | Q(notice_location__icontains=search) |
        Q(notice_message_num__icontains=search) | Q(notice_time__icontains=search))
        # if delete:
        #     # queryset = NoticeManager.objects.filter(id=delete)
        #     queryset = NoticeManager.objects.filter(id=delete)
        #     for Notice in queryset:
        #        Notice.is_delete = 1
        #        Notice.save()
        if id:
            queryset = NoticeManager.objects.filter(id=id, is_delete=0)
            if status:
                NoticeManager.objects.filter(id=id).update(
                    notice_status=status)
            if delete:
                NoticeManager.objects.filter(id=id).update(
                    is_delete=delete)

        return queryset

# class  LogViewSet(viewsets.ModelViewSet):
#     # 指定结果集并设置排序
#     queryset = Log_list.objects.all().order_by('-id')
#
#     serializer_class = Log_listSerializers
#     pagination_class = PageSet
#     # 配置搜索功能
#     filter_backends = (filters.SearchFilter,)
#     # 设置搜索的关键字
#     search_fields = ('=create_time', 'log_no')
#     # 设置搜索出的结果中需要排序的字段
#     ordering_field = ('create_time', 'log_no')


@api_view(['GET', 'POST'])
def getlispic(request, format=None,):
    if request.method == "GET":
        type = request.GET.get("type")
        start_time = request.GET.get("start_time")
        end_time = request.GET.get("end_time")
        print(type, start_time, end_time)
        if not type:
            return JsonResponse({
                "status_code": 0,
                "error": "you need have 'type'"
            })
        if not all([start_time, end_time]):
            db = Log_list.objects.filter(log_no=type).order_by("id")
            obj = PageSet()
            page_list = obj.paginate_queryset(db, request)
            ser = Log_listSerializers(instance=page_list, many=True)
            response = obj.get_paginated_response(ser.data)
            return response
        else:
            db = Log_list.objects.filter(log_no=type, create_time__gt=start_time,
                                         create_time__lt=end_time).order_by("id")
            obj = PageSet()
            page_list = obj.paginate_queryset(db, request)
            ser = Log_listSerializers(instance=page_list, many=True)
            response = obj.get_paginated_response(ser.data)
            return response

    if request.method == "POST":
        log_type = request.POST.get("log_type")
        log_leader = request.POST.get("log_leader")
        log_level = request.POST.get("log_level")
        log_info = request.POST.get("log_info")
        log_no = request.POST.get("log_no")
        data = dict()
        print(log_type, log_leader, log_level, log_info, log_no)
        if not all([log_type, log_leader, log_level, log_info, log_no]):
            return JsonResponse({
                "status_code": 0,
                "error": "you need have 'log_type,create_time'"
            })
        else:
            db = Log_list.objects.create(log_type=log_type, log_leader=log_leader, log_level=log_level, log_info=log_info,
                                         log_no=log_no)
            data = {"log_type":db.log_type, "log_leader":db.log_leader, "log_level":db.log_level, "log_info":db.log_info, "log_no":db.log_no}
            return HttpResponse("创建成功{}".format(data))












# # loginfo/getlog
def get_log(request):
    '''

    :param request:
    :return:
    '''
    if request.method == "GET":
        type = request.GET.get("type")
        start_time = request.GET.get("start_time")
        end_time = request.GET.get("end_time")
        pagination = request.GET.get("pagination")
        print(type,pagination, start_time, end_time)
        if not all([type]):
            return JsonResponse({
                "status_code": 0,
                "error": "you need have 'type'"
            })
        if not pagination:
            db = Log_list.objects.filter(log_no=type).order_by("id").reverse()[:10]
            json_db = json.loads(serializers.serialize("json", db))
            json_db = [row["fields"] for row in json_db]
            return JsonResponse({
                "status_code": 0,
                "db": json_db
            })
        else:
            if not all([start_time, end_time]):
                # 默認取前15條數據
                # db = Log_list.objects.filter(log_no=type).order_by("id").reverse()[:15]
                db = Log_list.objects.reverse()[:int(pagination)]
                json_db = json.loads(serializers.serialize("json", db))
                json_db = [row["fields"] for row in json_db]
                return JsonResponse({
                    "status_code": 0,
                    "db": json_db
                })
            else:
                
                # 篩選時間區域的
                db = Log_list.objects.filter(log_no=type, create_time__gt=start_time,
                                             create_time__lt=end_time).order_by("id").reverse()[:int(pagination)]
                json_db = json.loads(serializers.serialize("json", db))
                json_db = [row["fields"] for row in json_db]
                return JsonResponse({
                    "status_code": 0,
                    "db": json_db
                })


    if request.method == "POST":
        # a = "zyb"
        creat_data = request.POST.get("name",None)
        print(creat_data)
        # print((.fcreat_data))
        # print("你添加的出版社名称为：{0}".format(creat_data))
        # new_name = request.POST.get('username', None)
        if creat_data:
            # 【在数据库中新增一条】
            db= Name.objects.create(name=creat_data)
            # 跳转页面到用户列表页
            return JsonResponse({
                "status_code": 0,
                "db": db
            })
        else:
            print('不能为空')
            return JsonResponse({
                "status_code": 0,
                "db": "error"
            })



def get_name(request):
    users = Log_list.objects.all()
    # for user in users:
    log_type = request.GET.get('log_type')
    log_leader = request.GET.get('log_leader')
    log_level = request.GET.get('log_level')
    log_info = request.GET.get('log_info')
    log_no = request.GET.get('log_no')
    create_time = request.GET.get('create_time')
    end_time = request.GET.get('end_time')
    user_list = []
    if log_type:
        users = Log_list.objects.filter(log_type=log_type)
    if log_leader:
        users = Log_list.objects.filter(log_leader=log_leader)
    if log_level:
        users = Log_list.objects.filter(log_level=log_level)
    if log_info:
        users = Log_list.objects.filter(log_info=log_info)
    if log_no:
        users = Log_list.objects.filter(log_no=log_no)
    for user in users:
        # if create_time != None and end_time!= None:
        if end_time is not None and create_time is not None:
            if len(end_time) == 17 and len(create_time) == 17:
                # if create_time < str(user.create_time) < end_time:
                if create_time < str(user.create_time) < end_time:
                    print(str(user.create_time))
                    print(len(end_time))
                    user_list.append({
                        u'文件名': user.log_type,
                        u'管理者': user.log_leader,
                        u'日志级别': user.log_level,
                        u'描述': user.log_info,
                        u'日志类型': user.log_no,
                        u'時間': user.create_time,
                    })
            else:
                error = "數據格式不對"
                user_list.append(error)
            user_list = user_list.copy()
        elif end_time is None and create_time is None:
            user_list.append({
                u'文件名': user.log_type,
                u'管理者': user.log_leader,
                u'日志级别': user.log_level,
                u'描述': user.log_info,
                u'日志类型': user.log_no,
                u'時間': user.create_time,
            })
        else:
            print("error")
    return JsonResponse(user_list, safe=False)







