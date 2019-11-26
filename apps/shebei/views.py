import json

import time

from django.http import JsonResponse, Http404, HttpResponseRedirect
# from django.shortcuts import render
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.response import Response
from django.views.generic import View
from rest_framework import status
# from shebei.models import SubDevice
from apps.apidata.models import CollectData
from apps.qudong.models import EquipmentTemplateRtu
from apps.shebei.models import SubDevice
from apps.shebei.serializers import DataTransmitListSerializer
from apps.shebei.models import DataTransmitList
from django_redis import get_redis_connection
# from celery_tasks.tasks import transmit_for_mqtt, transmit_for_corepro
from .tasks import transmit_for_mqtt, transmit_for_corepro
from django.db.models import Avg, Sum, Max, Min, Count
from apps.qudong.tasks import Drive_modebusrtu
from apps.wangguang.tasks import Agent_sys_init_tasks

import re
# Create your views here.

# /index ^$
class DeviceView(View):
    '''主页'''
    def get(self,request):
        # 显示网关信息
        return render(request, 'index.html')

# shebei/devicelist
class DeviceListView(View):
    '''设备列表'''
    def get(self, request):
        # 显示设备列表
        subdevices = SubDevice.objects.all().order_by('-id')
        # print(subdevices)
        context = {
            "subdevices": subdevices
        }
        return render(request, 'shebei/Sub_Device_List.html', context)

    def post(self, request):
        '''添加子设备'''
        device_name=request.POST.get("device_name")
        device_type=request.POST.get("device_type")
        device_position=request.POST.get("device_position")
        device_model=request.POST.get("device_model")
        device_describe=request.POST.get("device_describe")
        # 进行参数校验
        if not all([device_name,device_type,device_position,device_model,device_describe]):
            subdevices = SubDevice.objects.all().order_by('-id')
            # print(subdevices)
            context = {
                "subdevices": subdevices
            }

            return render(request, 'shebei/Sub_Device_List.html', context)

        try:
            subdevice=SubDevice.objects.get(subdevice_name=device_name)
            '''网关名存在 不可以注册'''
            subdevices = SubDevice.objects.all().order_by('-id')
            # print(subdevices)
            context = {
                "subdevices": subdevices
            }

            return render(request, 'shebei/Sub_Device_List.html', context)
        except SubDevice.DoesNotExist:
            '''网关名不存在 既可以注册'''
            subdevice=SubDevice.objects.create(subdevice_name=device_name,
                                     subdevice_type=device_type,
                                     subdevice_position=device_position,
                                     subdevice_model=device_model,
                                     subdevice_remark=device_describe)
            subdevice.save()

            subdevices=SubDevice.objects.all().order_by('-id')
            # print(subdevices)
            context={
                "subdevices": subdevices
            }

            return render(request, 'shebei/Sub_Device_List.html', context)

# shebei/devicemanage  /device_id
class DeviceManageView(View):
    '''设备detail'''
    def get(self, request, device_id):
        # 显示设备列表
        subdevice=SubDevice.objects.filter(id=device_id)[0]
        transmits = DataTransmitList.objects.filter(subdevice_id=device_id).order_by('-id')[0:4]
        context={
            "subdevice": subdevice,
            "transmits": transmits
            # 'menu':1
        }
        return render(request, 'shebei/Sub_Device_Main.html', context)
    def post(self, request, device_id):
        '''post请求添加一条路径记录'''
        transmit_name = request.POST.get("transmit_name")
        transmit_type = request.POST.get("transmit_type")
        transmit_remark = request.POST.get("transmit_remark")
        transmit_ip = request.POST.get("transmit_ip")
        transmit_port = request.POST.get("transmit_port")
        transmit_username = request.POST.get("transmit_username")
        transmit_password = request.POST.get("transmit_password")
        transmit_topic = request.POST.get("transmit_topic")
        try:
            subdevice=SubDevice.objects.get(id=int(device_id))
        except SubDevice.DoesNotExist:
            '''不存在返回id'''
            return redirect(reverse('shebei:devicemanage', args=(device_id,)))

        #数据校验
        if not all([transmit_name, transmit_type, transmit_remark, transmit_ip,
                transmit_port, transmit_username, transmit_password, transmit_topic]):
            '''数据不完整'''
            return redirect(reverse('shebei:devicemanage', args=(device_id,)))
        #业务处理
        transmit = DataTransmitList.objects.create(transmit_name=transmit_name,
                                                  transmit_type=DataTransmitList.TYPE_DICT_F[transmit_type],
                                                  transmit_remark=transmit_remark,
                                                  transmit_ip=transmit_ip,
                                                  transmit_port=transmit_port,
                                                  transmit_username=transmit_username,
                                                  transmit_password=transmit_password,
                                                  transmit_topic=transmit_topic,
                                                  subdevice=subdevice)

        #返回页面
        return redirect(reverse('shebei:devicemanage', args=(device_id,)))


# shebei/deviceinfo
class DeviceInfoView(View):
    '''设备信息'''
    def get(self, request, device_id=None):
        # 显示单个设备的信息
        subdevice = SubDevice.objects.filter(id=device_id)[0]
        context = {
            "subdevice": subdevice
        }
        return render(request, 'shebei/Sub_Device_Information.html', context)


# /shebei/deviceprotocol/apply
class DeviceProtocolApi(View):
    '''
    处理保存设备的采集协议配置
    '''
    def post(self, request):
        subdevice_id=request.POST.get("subdevice_id")
        etr_name=request.POST.get("etr_name")
        template = EquipmentTemplateRtu.objects.filter(etr_name=etr_name)

        check=request.POST.get("parity_check")
        com=request.POST.get("acq_serial_slogans")
        databit=request.POST.get("data_bits")
        botelv=request.POST.get("baud_rate")
        stopbit=request.POST.get("stop_bit")
        timeout=request.POST.get("time_out")
        cycletime=request.POST.get("cycle_time")
        code=request.POST.get("code")
        drive=request.POST.get("qudong")
        info = [com, databit, botelv, check, stopbit, timeout, cycletime, code]
        print(subdevice_id, etr_name, info)
        # 第一步 数据校验
        if not all([com, databit, botelv, check, stopbit, timeout, cycletime, code, drive]):
            return JsonResponse({'res': 0, 'errmsg': '1111'})

        cmd_dict = self.join(template, code)
        print(cmd_dict)

        # 第二步 业务处理
        conn = get_redis_connection('default')
        key = "template_{}".format(subdevice_id)

        conn.hset(key, "enable", 0)
        # 等待任务停止
        conn.hset(key, "com", com)
        conn.hset(key, "botelv", botelv)
        conn.hset(key, "databit", databit)
        conn.hset(key, "check", check)
        conn.hset(key, "stopbit", stopbit)
        conn.hset(key, "timeout", timeout)
        conn.hset(key, "cycletime", cycletime)
        conn.hset(key, "code", code)
        conn.hset(key, "drive", drive)
        conn.hset(key, "etr_name", etr_name)

        # 第三步 返回结果
        # 调用采集驱动任务
        result = Drive_modebusrtu.apply_async(args=(subdevice_id, info, cmd_dict), queue= "worker_queue")
        conn.hset(key, "task_id", result)


        print("delay su1")
        return JsonResponse({'res': 3, 'message': '更新成功'})

    def join(self, template, code):
        '''
        return a dict
        keys : param
        value: cmd 01 03 00 01 00 02 无校验码
        '''
        cmd_dict = {}
        for i in template:
            cmd_dict[i.etr_param] =[''.join(["%02X"%int(code), i.etr_cmdid, i.etr_cmdregister, "%04X"%int(i.etr_cmdnumber)]),
                                    i.etr_format,
                                    i.etr_rule]
        return cmd_dict



# shebei/deviceprotocol
class DeviceProtocolView(View):
    '''采集协议'''
    def get(self, request, device_id):
        # 显示单个设备采集协议配置的信息
        device_id = device_id
        # etr = EquipmentTemplateRtu.objects.filter(etr_accordname="ModeBus-RTU").annotate(num=Count("etr_name"))
        etrs = EquipmentTemplateRtu.objects.values("etr_accordname", "etr_name").annotate(num=Count("etr_name"))
        # print(etrs)
        templates=[]
        addrs = []
        for addr in range(247):
            addrs.append(addr)
        for etr in etrs:
            template = EquipmentTemplateRtu.objects.filter(etr_accordname="ModeBus-RTU",etr_name=etr["etr_name"])
            templates.append(template)
        # print(templates)
        return render(request, 'shebei/Acquisition_Protocol.html', locals())

    def post(self,request, device_id):
        template_name=request.POST.get("template_name")
        template_description=request.POST.get("template_description")
        cmd_id=request.POST.getlist("cmd_id")
        register_address=request.POST.getlist("register_address")
        register_num=request.POST.getlist("register_num")
        register_param=request.POST.getlist("register_param")
        data_rule=request.POST.getlist("rule")
        data_format=request.POST.getlist("format")
        for index, val in enumerate(cmd_id):
            template=EquipmentTemplateRtu.objects.create(etr_name = template_name,
                                                etr_remark = template_description,
                                                etr_cmdid = cmd_id[index],
                                                etr_cmdregister = "%04X"%(int(register_address[index])),
                                                etr_cmdnumber = register_num[index],
                                                etr_param = register_param[index],
                                                etr_format = EquipmentTemplateRtu.FORMAT_DICT[data_format[index]],
                                                etr_rule= data_rule[index])
            template.save()
            print("save success")
        etrs = EquipmentTemplateRtu.objects.values("etr_accordname", "etr_name").annotate(num=Count("etr_name"))
        # print(etrs)
        templates = []
        addrs = []
        for addr in range(247):
            addrs.append(addr)
        for etr in etrs:
            template = EquipmentTemplateRtu.objects.filter(etr_accordname="ModeBus-RTU", etr_name=etr["etr_name"])
            templates.append(template)
        print(templates)
        return render(request, 'shebei/Acquisition_Protocol.html', locals())
        # return render(request, 'shebei/Acquisition_Protocol.html')


# shebei/devicededug
class DeviceDebugView(View):
    '''设备调试'''
    def get(self, request, device_id):
        # 显示单个设备的调试信息
        subdevice = SubDevice.objects.filter(id=device_id)[0]
        subdevice_name = subdevice.subdevice_name
        subdevice_position = subdevice.subdevice_position
        subdevice_type = subdevice.subdevice_type
        conn = get_redis_connection('default')
        key = "template_{}".format(device_id)
        try:
            com =conn.hget(key, "com").decode()
            botelv =conn.hget(key, "botelv").decode()
            databit =conn.hget(key, "databit").decode()
            check =conn.hget(key, "check").decode()
            stopbit = conn.hget(key, "stopbit").decode()
            timeout =conn.hget(key, "timeout").decode()
            cycletime =conn.hget(key, "cycletime").decode()
            code =conn.hget(key, "code").decode()
            drive = conn.hget(key, "drive").decode()
            etr_name = conn.hget(key, "etr_name").decode()
            data = CollectData.objects.filter(id=device_id).order_by("-id")[0]
            template_data = json.loads(data.data)
            print(template_data)
            select = conn.hget(key, "selected")
            if select:
                generate_template={}
                select=eval(select.decode())
                for temp in template_data:
                    if temp in select:
                        generate_template[temp] = template_data[temp]

        except:
            print("未配置协议")


        return render(request, 'shebei/Equipment_Debugging.html', locals())

# shebei/devicedataforward
class DeviceDataView(View):
    '''设备信息'''
    def get(self, request, device_id):
        # 显示单个设备的数据转发信息
        transmits = DataTransmitList.objects.filter(subdevice_id=device_id).order_by('-id')[0:4]
        conn = get_redis_connection('default')
        transmit_count_list=[]
        for transmit in transmits:
            # print(transmit.id)
            transmit_key = 'transmit_count_%d_%d' %(int(device_id), int(transmit.id))
            try:
                transmit_count = int(conn.get(transmit_key))
            except:
                transmit_count = 0
            transmit_count_list.append(transmit_count)

        context = {
            "transmits": transmits,
            'transmit_count_list': transmit_count_list,
        }
        print(context)
        return render(request, 'shebei/Data_Forwarding.html', context)

    def post(self, request, device_id):
        '''post请求添加一条路径记录'''
        transmit_name = request.POST.get("transmit_name")
        transmit_type = request.POST.get("transmit_type")
        transmit_remark = request.POST.get("transmit_remark")
        transmit_ip = request.POST.get("transmit_ip")
        transmit_port = request.POST.get("transmit_port")
        transmit_username = request.POST.get("transmit_username")
        transmit_password = request.POST.get("transmit_password")
        transmit_topic = request.POST.get("transmit_topic")
        try:
            subdevice = SubDevice.objects.get(id=int(device_id))
        except SubDevice.DoesNotExist:
            '''不存在返回id'''
            print( '''不存在返回id''')
            return redirect(reverse('shebei:devicedataforward', args=(device_id,)))

        # 数据校验
        if not all([transmit_name, transmit_type, transmit_remark, transmit_ip,
                    transmit_port, transmit_username, transmit_password, transmit_topic]):
            '''数据不完整'''
            print('''数据不完整''')
            return redirect(reverse('shebei:devicedataforward', args=(device_id,)))
        # 业务处理
        transmit = DataTransmitList.objects.create(transmit_name=transmit_name,
                                                   transmit_type=DataTransmitList.TYPE_DICT_F[transmit_type],
                                                   transmit_remark=transmit_remark,
                                                   transmit_ip=transmit_ip,
                                                   transmit_port=transmit_port,
                                                   transmit_username=transmit_username,
                                                   transmit_password=transmit_password,
                                                   transmit_topic=transmit_topic,
                                                   subdevice=subdevice)

        # 返回页面
        return redirect(reverse('shebei:devicedataforward', args=(device_id,)))


# /shebei/transmit/modify
class TransmitModifyApi(View):
    '''修改编辑转发路径'''

    def post(self, request):
        '''修改设备信息'''
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 0, 'errmsg': '请先登录'})
        transmit_id = request.POST.get("transmit_id")
        transmit_name = request.POST.get("transmit_name")
        transmit_type = request.POST.get("transmit_type")
        transmit_remark = request.POST.get("transmit_remark")
        transmit_ip = request.POST.get("transmit_ip")
        transmit_port = request.POST.get("transmit_port")
        transmit_username = request.POST.get("transmit_username")
        transmit_password = request.POST.get("transmit_password")
        transmit_topic = request.POST.get("transmit_topic")
        print([transmit_id,transmit_name, transmit_type, transmit_remark, transmit_ip,
                    transmit_port, transmit_username, transmit_password, transmit_topic])
        # 数据校验
        if not all([transmit_id,transmit_name, transmit_type, transmit_remark, transmit_ip,
                    transmit_port, transmit_username, transmit_password, transmit_topic]):
            '''数据不完整'''
            print('''数据不完整''')
            return JsonResponse({'res': 1, 'errmsg': '数据不完整'})
        transmit = DataTransmitList.objects.get(id=int(transmit_id))
        # 业务处理
        transmit.transmit_name=transmit_name
        # transmit.transmit_type=transmit.TYPE_DICT_F[transmit_type]
        transmit.transmit_type=int(transmit_type)
        transmit.transmit_remark=transmit_remark
        transmit.transmit_ip=transmit_ip
        transmit.transmit_port=transmit_port
        transmit.transmit_username=transmit_username
        transmit.transmit_password=transmit_password
        transmit.transmit_topic=transmit_topic
        transmit.save()

        # 返回页面
        return JsonResponse({'res': 2, 'message': 'transmit修改成功'})

# /shebei/transmit/update
class TransmitUpdateApi(View):
    '''设备更新状态'''
    def post(self, request):
        '''修改设备的状态启用禁用信息'''
        user = request.user
        # print(user)
        if not user.is_authenticated:
            return JsonResponse({'res': 0, 'errmsg': '请先登录'})

        # 校验数据
        result = self.check_data(request)
        if result["res"] == 2:
            #数据校验没问题
            cache = self.get_cache(result["data"])
            subdevice_enable = int(cache["subdevice_enable"])
            transmit_enable = int(cache["transmit_enable"])
            transmit_type = int(cache["transmit_type"])
            if subdevice_enable:
                #设备正常
                transmit_mqtt_list, transmit_corepro_list = self.update_status(cache, cache["transmit_key"], transmit_enable)
                if transmit_enable:
                    # 符合条件去开启转发驱动任务
                    # 不同类型的驱动配置启动不同的配置
                    self.delay_task(transmit_type, transmit_mqtt_list, transmit_corepro_list)

                else:
                    #要去停止转发驱动
                    #更新mysql redis 的数据状态
                    print(cache["transmit_id"] ,"transmit stop")
            else:
                # 设备禁用的情况下不启动驱动
                print("subdevice stop")
                return JsonResponse({'res': 2, 'errmsg': '设备已禁用'})
        else:
            # 数据校验失败
            return JsonResponse(result)
        # 数据更新成功
        return JsonResponse({'res': 3, 'message': '更新成功', "transmit_enable":transmit_enable})


    def check_data(self, request):
        # 接收数据
        subdevice_id = request.POST.get('subdevice_id')
        transmit_id = request.POST.get('transmit_id')
        transmit_type = request.POST.get('transmit_type')
        transmit_enable = request.POST.get('transmit_enable')
        # 数据校验
        if not all([subdevice_id, transmit_id, transmit_type, transmit_enable]):
            return {'res': 1, 'errmsg': '数据不完整'}

        else:
            return { 'res': 2,
                     'message': '数据校验正常',
                     "data": {"subdevice_id":subdevice_id,
                              "transmit_id":transmit_id,
                              "transmit_type":transmit_type,
                              "transmit_enable":transmit_enable }
                     }

    def get_cache(self, data):
        self.conn = get_redis_connection('default')
        transmit_key = "transmit_%d_%d" % (int(data["subdevice_id"]), int(data["transmit_id"]))
        subdevice_key = "subdevice_%d" % int(data["subdevice_id"])
        count_key = "transmit_count_%d_%d" % (int(data["subdevice_id"]), int(data["transmit_id"]))
        status_key = "transmit_status_%d_%d" % (int(data["subdevice_id"]), int(data["transmit_id"]))


        subdevice_enable = self.conn.get(subdevice_key)
        if subdevice_enable is None:
            subdevice_enable = 1
            self.conn.set(subdevice_key, subdevice_enable)

        # 每一条转发路径的转发条数
        transmit_count = self.conn.get(count_key)
        if transmit_count is None:
            transmit_count = 0
            self.conn.set(count_key, transmit_count)

        # 每一条转发路径的状态
        transmit_status = self.conn.get(status_key)
        if transmit_status is None:
            transmit_status = "正在运行"
            self.conn.set(status_key, transmit_status)

        data.update({"subdevice_enable":subdevice_enable,
                     "transmit_count": transmit_count,
                     "transmit_status": transmit_status,
                     "transmit_key": transmit_key,
                     "subdevice_key":subdevice_key,
                     "count_key":count_key,
                     "status_key":status_key
                    })
        return data

    def update_status(self, cache, transmit_key, transmit_enable):
        # 更新数据和缓存的数据
        self.conn.set(transmit_key,transmit_enable)
        print(transmit_key,transmit_enable)
        transmit = DataTransmitList.objects.get(id=int(cache["transmit_id"]))
        transmit.transmit_enable = transmit_enable
        if transmit_enable == 1:
            transmit.transmit_status = 0
            transmit_status = "正在运行"
            self.conn.set(cache["status_key"], transmit_status)
        else:
            transmit.transmit_status = 3
            transmit_status = "转发停止"
            self.conn.set(cache["status_key"], transmit_status)

        transmit_ip = transmit.transmit_ip
        transmit_port = transmit.transmit_port
        transmit_username = transmit.transmit_username
        transmit_password = transmit.transmit_password
        transmit_topic = transmit.transmit_topic
        transmit.save()
        subdevice = SubDevice.objects.get(id=int(cache["subdevice_id"]))
        transmit_mqtt_list = [cache["count_key"], cache["subdevice_key"], transmit_key, transmit_ip, transmit_port,
                              transmit_username, transmit_password, transmit_topic]
        transmit_corepro_list = [cache["count_key"], cache["subdevice_key"], transmit_key, subdevice.subdevice_name,
                                 subdevice.subdevice_key,subdevice.subdevice_secret]
        return transmit_mqtt_list, transmit_corepro_list

    def delay_task(self, transmit_type, transmit_mqtt_list, transmit_corepro_list):
        # 触发任务
        if transmit_type == 0:
            print(transmit_mqtt_list)
            print("MQTT delay task")
            transmit_for_mqtt.delay(*transmit_mqtt_list)

        elif transmit_type == 1:
            print(transmit_corepro_list)
            print("CorePro delay task")
            transmit_for_corepro.delay(*transmit_corepro_list)

        elif transmit_type == 2:
            # print(transmit_list)
            print("KAFKA delay task")
        elif transmit_type == 3:
            # print(transmit_list)
            print("DB delay task")


# shebei/modify
class DeviceModifyApi(View):
    def post(self, request):
        '''修改设备信息'''
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 0, 'errmsg': '请先登录'})
        # 接收数据
        subdevice_id = request.POST.get('subdevice_id')
        subdevice_name = request.POST.get('subdevice_name')
        subdevice_type = request.POST.get('subdevice_type')
        subdevice_model = request.POST.get('subdevice_model')
        subdevice_position = request.POST.get('subdevice_position')
        subdevice_remark = request.POST.get('subdevice_remark')
        print([subdevice_id,subdevice_name,subdevice_type,subdevice_model,subdevice_position,subdevice_remark])
        # 数据校验
        if not all([subdevice_id,subdevice_name,subdevice_type,subdevice_model,subdevice_position,subdevice_remark]):
            return JsonResponse({'res': 1, 'errmsg': '数据不完整'})

        device = SubDevice.objects.get(id= int(subdevice_id))
        device.subdevice_name=subdevice_name
        device.subdevice_type=subdevice_type
        device.subdevice_model=subdevice_model
        device.subdevice_position=subdevice_position
        device.subdevice_remark=subdevice_remark
        device.save()
        return JsonResponse({'res': 2, 'message': '更新成功'})

# shebei/update
class DeviceUpdateApi(View):
    '''设备更新状态'''
    def post(self, request):
        '''修改设备的状态启用禁用信息'''
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 0, 'errmsg': '请先登录'})

        # 接收数据
        subdevice_id = int(request.POST.get('device_id'))
        subdevice_enable = request.POST.get('device_enable')

        conn = get_redis_connection('default')
        # cart_key = 'cart_%d' % user.id
        # transmit_key = "transmit_%d_%d" % (subdevice_id, transmit_id)
        subdevice_key = "subdevice_%d" % subdevice_id
        # subdevice_enable = conn.get(subdevice_key)
        conn.set(subdevice_key, int(subdevice_enable))
        print(subdevice_key, subdevice_enable)
        # 数据校验
        if not all([subdevice_id,subdevice_enable]):
            return JsonResponse({'res': 1, 'errmsg': '数据不完整'})

        device = SubDevice.objects.get(id= int(subdevice_id))
        device.subdevice_enable= int(subdevice_enable)
        device.save()
        return JsonResponse({'res': 2, 'message': '更新成功'})

# shebei/delete
class DeviceDeleteApi(View):
    '''删除设备'''

    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 0, 'errmsg': '请先登录'})

        # 接收参数
        device_id = request.POST.get('id')
        # 数据校验
        if not device_id:
            print('无效的设备id')
            return JsonResponse({'res': 1, 'errmsg': '无效的设备id'})

        # 校验商品是否存在
        try:
            device = SubDevice.objects.get(id=int(device_id))
        except SubDevice.DoesNotExist:
            print("设备不存在")
            return JsonResponse({'res': 2, 'errmsg': '设备不存在'})

        # 业务处理: 删除记录
        device.delete()

        # conn = get_redis_connection('default')
        # cart_key = 'cart_%d' % user.id
        #
        # # 删除 hdel
        # conn.hdel(cart_key, sku_id)
        #
        # # 计算用户购物车中商品的总件数{'1':5,'2':3}
        # total_count = 0
        # vals = conn.hvals(cart_key)
        # for val in vals:
        #     total_count += int(val)
        print("删除成功")
        return JsonResponse({'res': 3, 'message': '删除成功'})

# shebei/transmit/delete
class TransmitDeleteApi(View):
    '''删除设备'''

    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 0, 'errmsg': '请先登录'})

        # 接收参数
        transmit_id = request.POST.get('transmit_id')

        # 数据校验
        if not transmit_id:
            return JsonResponse({'res': 1, 'errmsg': '无效的数据id'})

        # 校验商品是否存在
        try:
            transmit = DataTransmitList.objects.get(id=transmit_id)
        except DataTransmitList.DoesNotExist:
            return JsonResponse({'res': 2, 'errmsg': '数据不存在'})

        # 业务处理: 删除记录
        transmit.delete()

        # conn = get_redis_connection('default')
        # cart_key = 'cart_%d' % user.id
        #
        # # 删除 hdel
        # conn.hdel(cart_key, sku_id)
        #
        # # 计算用户购物车中商品的总件数{'1':5,'2':3}
        # total_count = 0
        # vals = conn.hvals(cart_key)
        # for val in vals:
        #     total_count += int(val)

        return JsonResponse({'res': 3, 'message': '删除成功'})


# shebei/transmit/count
class TransmitCountApi(View):
    '''计数'''

    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 0, 'errmsg': '请先登录'})

        # 接收参数
        subdevice_id = int(request.POST.get('subdevice_id'))
        transmit_id = int(request.POST.get('transmit_id'))
        # print(subdevice_id, transmit_id)

        # 数据校验
        if not transmit_id:
            return JsonResponse({'res': 1, 'errmsg': '无效的数据id'})

        # 校验商品是否存在
        try:
            transmit = DataTransmitList.objects.get(id=transmit_id)
        except DataTransmitList.DoesNotExist:
            return JsonResponse({'res': 2, 'errmsg': '数据不存在'})

        # 业务处理: 删除记录
        count_key = "transmit_count_%d_%d" % (int(subdevice_id), int(transmit_id))
        status_key = "transmit_status_%d_%d" % (int(subdevice_id), int(transmit_id))
        conn = get_redis_connection('default')
        transmit_count = conn.get(count_key)
        transmit_status = conn.get(status_key)
        # print(transmit_count)
        if transmit_count is None:
            transmit_count = 0
            conn.set(count_key, transmit_count)

        # conn = get_redis_connection('default')
        # cart_key = 'cart_%d' % user.id
        #
        # # 删除 hdel
        # conn.hdel(cart_key, sku_id)
        #
        # # 计算用户购物车中商品的总件数{'1':5,'2':3}
        # total_count = 0
        # vals = conn.hvals(cart_key)
        # for val in vals:
        #     total_count += int(val)

        return JsonResponse({'res': 3, 'count': transmit_count.decode() , 'status':transmit_status.decode() })
