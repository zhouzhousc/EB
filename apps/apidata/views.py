import json

from django.shortcuts import render, HttpResponse
# from apidata.models import CollectData
# from apidata.serializers import CollectDataSerializer
from rest_framework.reverse import reverse


from apps.apidata.models import CollectData, M5Data
from apps.apidata import serializers
from apps.apidata.serializers import CollectDataSerializer, M5DataSerializer, SubDeviceSerializer
from django.views.generic import View
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets

from django.http import JsonResponse
from apps.shebei.models import SubDevice
# from apps.user.models import User


class CollectDataViewSet(viewsets.ModelViewSet):
    """
    子设备 数据集所有的数据分页显示
    """
    queryset = CollectData.objects.all().order_by("id")
    # queryset = CollectData.objects.filter(data_status=0)
    serializer_class = CollectDataSerializer

class M5DataViewSet(viewsets.ModelViewSet):
    """
    M5 数据集所有的数据分页显示
    """
    queryset = M5Data.objects.all().order_by("id")
    serializer_class = M5DataSerializer

class SubDeviceViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    已注册的子设备详细信息列表
    '''
    queryset = SubDevice.objects.all().order_by("id")
    serializer_class = SubDeviceSerializer




class M5DataList(APIView):
    """
    所有的M5 设备CollectData或者创建一条新的数据。
    """
    def get(self, request, format=None):
        # datalist = M5Data.objects.all()
        datalist = M5Data.objects.all().order_by("-id")[0:10]
        serializer = M5DataSerializer(datalist, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = M5DataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# m5/notsend/<m5device>
class M5DataListForDevice(APIView):
    """
    检索一个M5设备的所有未发送的数据。 /apidata/m5/notsend/<m5device_name>
    用于转发模块使用 data_status=0 为未发送数据
    data_type=0 属性消息、data_type=1 事件消息、data_type=2 报警消息、
    """

    def get_object(self, m5device_name):
        try:
            # 过滤相同设备subdevice_id的数据 状态data_status为0 未发送的数据
            return M5Data.objects.filter(subdevice_name=m5device_name, data_status=0).reverse()[0:10]
        except CollectData.DoesNotExist:
            raise Http404

    # m5/notsend/<m5device_name> 1
    def get(self, request, m5device_name, format=None):
        devicedata = self.get_object(m5device_name)
        serializer = M5DataSerializer(devicedata, many=True)
        return Response(serializer.data)

    # 修改单个设备的一条消息 将data_status=0 改成 data_status=1 未发送改成已发送
    # /apidata/m5/notsend/<m5device_name>/<message_id>
    def post(self, request, m5device_name, message_id, format=None):
        try:
            devicedata = M5Data.objects.get(subdevice_name=m5device_name, data_status=0, id=message_id)
            # print(devicedata)
            devicedata.data_status = 1  # 修改
            devicedata.is_delete = True  # 确认删除 一天后
            devicedata.save()
            return JsonResponse({'res': 0, 'errmsg': '删除成功'})

        except CollectData.DoesNotExist:
            raise Http404

class M5DataListUpdate(APIView):
    '''
     get:查看单个设备所有已发送的数据 /apidata/send/<subdevice_id>
     data_status=1 为已发送数据
    data_type=0 属性消息、data_type=1 事件消息、data_type=2 报警消息、
     post: 获取该类型下的最新一条数据
    '''
    def get(self, request, m5device_name, format=None):
        devicedata = M5Data.objects.filter(subdevice_name=m5device_name, data_status=1)
        serializer = M5DataSerializer(devicedata, many=True)
        return Response(serializer.data)
    def post(self, request, m5device_name):
        try:
            # m5device_name= request.POST.get("m5device_name")
            print(m5device_name)
            m5data = M5Data.objects.filter(subdevice_name=m5device_name).order_by("-id")[0]
            data = json.loads(m5data.data)
            print(data)
            return JsonResponse({'res': 0, 'data': data})

        except Exception as e:
            return JsonResponse({'res': 1, 'errmsg': str(e)})



class DataList(APIView):
    """
    所有的CollectData或者创建一条新的数据。
    """
    def get(self, request, format=None):
        datalist = CollectData.objects.all().order_by("-id")[0:10]
        serializer = CollectDataSerializer(datalist, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        try:
            subdevice=SubDevice.objects.get(id=request.data["subdevice_id"])
        except SubDevice.DoesNotExist:
            raise Http404

        serializer = CollectDataSerializer(data=request.data, context={"subdevice":subdevice})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#
class DataListForDevice(APIView):
    """
    检索一个设备的所有未发送的数据。 /apidata/notsend/<subdevice_id>
    用于转发模块使用 data_status=0 为未发送数据
    data_type=0 属性消息、data_type=1 事件消息、data_type=2 报警消息、
    """
    def get_object(self, subdevice_id):
        try:
            #过滤相同设备subdevice_id的数据 状态data_status为0 未发送的数据
            return CollectData.objects.filter(subdevice_id=subdevice_id, data_status=0).order_by("-id")[0:10]
        except CollectData.DoesNotExist:
            raise Http404

    def get(self, request, subdevice_id, format=None):
        devicedata = self.get_object(subdevice_id)
        serializer = CollectDataSerializer(devicedata, many=True)
        return Response(serializer.data)

    # 修改单个设备的一条消息 将data_status=0 改成 data_status=1 未发送改成已发送
    # /apidata/notsend/<subdevice_id>/<message_id>
    def post(self, request, subdevice_id, message_id, format=None):
        try:
            devicedata = CollectData.objects.get(subdevice_id=subdevice_id, data_status=0, id=message_id)
            # print(devicedata)
            devicedata.data_status = 1  # 修改
            devicedata.is_delete = True  # 确认删除 一天后
            devicedata.save()
            # devicedata = self.get_object(subdevice_id)
            # serializer = CollectDataSerializer(devicedata, many=True)
            # return Response(serializer.data)
            return JsonResponse({'res': 0, 'errmsg': '删除成功'})

        except CollectData.DoesNotExist:
            raise Http404



class DataListUpdate(APIView):
    '''
    查看单个设备所有已发送的数据 /apidata/send/<subdevice_id>
     data_status=1 为已发送数据
    data_type=0 属性消息、data_type=1 事件消息、data_type=2 报警消息、
    '''
    def get(self, request, subdevice_id, format=None):
        devicedata = CollectData.objects.filter(subdevice_id=subdevice_id, data_status=1).order_by("-id")[0:10]
        serializer = CollectDataSerializer(devicedata, many=True)
        return Response(serializer.data)


class DataListDelete(APIView):
    '''
    删除所有设备已发送的数据  /apidata/send/delete
    '''
    def get_object(self):
        try:
            return CollectData.objects.get(is_delete=True)
        except CollectData.DoesNotExist:
            raise Http404

    def delete(self, request, format=None):
        devicedata = self.get_object()
        devicedata.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
