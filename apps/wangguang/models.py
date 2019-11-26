from django.db import models
from db.base_model import BaseModel

# Create your models here.


class RegisterInfo(BaseModel):
    '''网关产品注册信息模型类'''
    gateway_name= models.CharField(max_length=30, verbose_name="网关唯一名称")
    gateway_key= models.CharField(max_length=100, verbose_name="网关id")
    gateway_secret= models.CharField(max_length=200, verbose_name="网关秘钥")
    gateway_authurl= models.CharField(max_length=200, verbose_name="网关鉴权URl")
    gateway_subdevice_num= models.IntegerField(default=1, verbose_name="网关子设备数量")
    gateway_model= models.CharField(max_length=30, verbose_name="网关型号")
    gateway_trade_name= models.CharField(max_length=30, verbose_name="网关厂商名称")
    gateway_registration_time= models.DateTimeField(verbose_name="网关注册时间")
    gateway_location= models.CharField(max_length=30, verbose_name="网关位置信息")
    gateway_reset_time= models.DateTimeField(verbose_name="网关最近恢复出厂日期")
    gateway_remark= models.CharField(max_length=50,verbose_name="网关描述")

    class Meta:
        db_table = 'gateway_register_info'
        verbose_name = '网关产品注册信息'
        verbose_name_plural = verbose_name

class SysInfo(BaseModel):
    '''网关系统信息模型类'''
    NET_STATUS_CHOICES = (
        (0, '网络状态正常'),
        (1, '网络状态')
    )
    sys_hostname= models.CharField(max_length=30, verbose_name="系统主机用户名称")
    sys_product_name= models.CharField(max_length=30, verbose_name="产品名称")
    sys_os= models.CharField(max_length=30, verbose_name="系统运行环境")
    sys_ip= models.CharField(max_length=30, verbose_name="系统网络IP地址")
    sys_mac= models.CharField(max_length=30, verbose_name="系统网络MAC地址")
    sys_mask= models.CharField(max_length=30, verbose_name="系统网络子网掩码")
    sys_gateway= models.CharField(max_length=30, verbose_name="系统网络默认网关")
    sys_net_status= models.SmallIntegerField(default=0, choices=NET_STATUS_CHOICES, verbose_name="系统网络状态")
    sys_rateof_cpu= models.CharField(max_length=30, verbose_name="系统CPU使用率")
    sys_memory= models.CharField(max_length=30, verbose_name="系统当前剩余内存")
    sys_memory_size= models.CharField(max_length=30, verbose_name="系统内存大小")
    sys_harddisk= models.CharField(max_length=30, verbose_name="系统当前剩余硬盘大小")
    sys_harddisk_size= models.CharField(max_length=30, verbose_name="系统硬盘大小")
    sys_usb_num= models.IntegerField(default=4, verbose_name="系统USB接口数量")
    sys_rs232_num= models.IntegerField(default=2, verbose_name="系统rs232接口数量")
    sys_use_usb_num= models.IntegerField(null=True,default=4, verbose_name="系统USB使用數量")
    sys_com = models.CharField(null=True,max_length=30, verbose_name="當前COM口")
    sys_running_time= models.CharField(default="0秒", max_length=30, verbose_name="系统运行时间")
    sys_local_time= models.DateTimeField(verbose_name="系统本地时间")
    sys_out_time= models.DateTimeField(verbose_name="系统出厂时间")
    sys_net_model= models.CharField(max_length=30, verbose_name="系统网络模块")

    def __unicode__(self):
        return '%d: %s' % (self.pk, self.sys_product_name)

    class Meta:
        db_table = 'gateway_sys_info'
        verbose_name = '网关系统信息'
        verbose_name_plural = verbose_name
