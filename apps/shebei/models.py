import datetime

from django.db import models
from db.base_model import BaseModel
# Create your models here.


class SubDevice(BaseModel):
    '''子设备列表模型类'''
    ENABLE_CHOICES=(
        (0, "未启用"),
        (1, "启用")
    )
    STATUS_CHOICES=(
        (0, "离线"),
        (1, "在线"),
    )
    subdevice_name= models.CharField(max_length=30, verbose_name="子设备名称")
    subdevice_key= models.CharField(default="", max_length=100, verbose_name="子设备id")
    subdevice_secret= models.CharField(default="", max_length=200, verbose_name="子设备secret")
    subdevice_position= models.CharField(max_length=30, verbose_name="子设备位置")
    subdevice_model= models.CharField(max_length=30, verbose_name="子设备型号")
    subdevice_type= models.CharField(max_length=30, verbose_name="子设备类型")
    subdevice_remark= models.CharField(max_length=50, verbose_name="子设备描述")
    subdevice_online_time= models.DateTimeField(auto_now_add=True, verbose_name="最近上线时间")
    subdevice_status= models.SmallIntegerField(default=0, choices=STATUS_CHOICES, verbose_name="子设备运行状态")
    subdevice_enable= models.SmallIntegerField(default=1, choices=ENABLE_CHOICES, verbose_name="子设备激活使能")

    class Meta:
        db_table = 'gateway_subdevice_list'
        verbose_name = '网关子设备列表信息'
        verbose_name_plural = verbose_name


class DataTransmitList(BaseModel):
    '''子设备列表模型类'''
    TYPE=(
        (0, "CorePro"),
        (1, "MQTT"),
        (2, "KAFKA"),
        (3, "DB"),
    )
    TYPE_DICT_F = { "MQTT":0, "CorePro":1,"KAFKA":2,"DB":3}
    TYPE_DICT = { 0:"MQTT", 1:"CorePro",2:"KAFKA",3:"DB"}
    STATUS_DICT = { 0:"正在运行", 1:"已禁用",2:"转发出错",3:"转发停止"}

    STATUS = (
        (0, "正在运行"),
        (1, "已禁用"),
        (2, "运行异常"),
        (3, "转发停止"),
    )
    ENABLE_CHOICES = (
        (0, "关闭"),
        (1, "启用")
    )
    subdevice = models.ForeignKey('shebei.SubDevice', to_field='id', on_delete=models.CASCADE, verbose_name='子设备id')
    transmit_type = models.SmallIntegerField(default=0, choices=TYPE, verbose_name="转发类型")
    transmit_status = models.SmallIntegerField(default=1, choices=STATUS, verbose_name="转发状态")
    transmit_name = models.CharField(default="通道xx",max_length=30, verbose_name="转发名称")
    transmit_remark = models.CharField(default="通道xx",max_length=30, verbose_name="转发描述")
    transmit_ip = models.CharField(default="",max_length=30, verbose_name="转发ip")
    transmit_port = models.CharField(default="",max_length=30, verbose_name="转发port")
    transmit_username = models.CharField(default="",max_length=100, verbose_name="转发用户")
    transmit_password = models.CharField(default="",max_length=100, verbose_name="转发密码")
    transmit_topic = models.CharField(default="",max_length=100, verbose_name="转发主题或表")
    transmit_number= models.IntegerField(default=0, verbose_name="子设备上传消息数")
    transmit_enable= models.SmallIntegerField(default=0, choices=ENABLE_CHOICES, verbose_name="子设备激活使能")

    class Meta:
        db_table = 'gateway_transmit_list'
        verbose_name = '网关子设备数据转发通道'
        verbose_name_plural = verbose_name