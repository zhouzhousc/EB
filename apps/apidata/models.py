import json

from django.db import models

# Create your models here.
from django.db import models
from db.base_model import BaseModel

class CollectData(BaseModel):
    '''采集的数据表模型类'''
    DATATYPE=(
        (0, "属性"),
        (1, "事件"),
        (2, "报警"),
    )
    DATASTATUS=(
        (0, "未发送"),
        (1, "已发送"),
    )
    # subdevice_id= models.IntegerField(verbose_name="子设备id")
    subdevice= models.ForeignKey('shebei.SubDevice',related_name="collectdatas", to_field='id', on_delete=models.CASCADE, verbose_name='子设备id')
    data_type= models.SmallIntegerField(default=0, choices=DATATYPE, verbose_name="子设备数据类型")
    data_status= models.SmallIntegerField(default=0, choices=DATASTATUS, verbose_name="数据状态")
    data= models.CharField(max_length=2000, verbose_name="子设备采集数据")
    class Meta:
        db_table = 'gateway_subdevice_collectdata'
        verbose_name = '网关子设备采集数据'
        verbose_name_plural = verbose_name

class M5Data(BaseModel):
    '''采集的M5数据表模型类'''

    DATATYPE = (
        (0, "属性"),
        (1, "事件"),
        (2, "报警"),
    )
    DATASTATUS = (
        (0, "未发送"),
        (1, "已发送"),
    )
    # subdevice_id= models.IntegerField(verbose_name="子设备id")
    subdevice_name = models.CharField(max_length=30, verbose_name='子设备name')
    data_type = models.SmallIntegerField(default=0, choices=DATATYPE, verbose_name="子设备数据类型")
    data_status = models.SmallIntegerField(default=0, choices=DATASTATUS, verbose_name="数据状态")
    data = models.CharField(max_length=2000, verbose_name="子设备采集数据")


    class Meta:
        db_table = 'gateway_m5_collectdata'
        verbose_name = 'M5网关子设备采集数据'
        verbose_name_plural = verbose_name

