from django.db import models
from db.base_model import BaseModel

# Create your models here.


class Drive(BaseModel):
    '''驱动程序管理模型类'''
    drive_name= models.CharField(max_length=30, verbose_name="驱动名称")
    drive_path= models.CharField(max_length=150, verbose_name="驱动路径")
    drive_remark= models.CharField(max_length=150, verbose_name="驱动描述")

    class Meta:
        db_table = 'gateway_drive_list'
        verbose_name = '网关子设备列表信息'
        verbose_name_plural = verbose_name

# 模板信息
class ModbusRtuModel(BaseModel):
    '''ModBus Rtu 协议配置模型 对应设备模板库 以及采集协议配置表单'''
    PARITY_CHECK_CHOICES= (
        (0, "ODD"),
        (1, "EVEN"),
        (2, "无校验"),
    )
    RULE_CHOICES= (
        (0, "长整型"),
        (1, "IEEE-754")
    )
    SHOW_CHOICES= (
        (0, "不显示至设备模板列表"),
        (1, "显示至设备模板列表")
    )
    # subdevice_id= models.IntegerField(verbose_name="子设备id")
    subdevice= models.ForeignKey('shebei.SubDevice', to_field='id', on_delete=models.CASCADE, verbose_name='子设备id')
    accord_name = models.CharField(max_length=30, verbose_name="协议名称")
    accord_type = models.CharField(max_length=30, verbose_name="协议类型")
    accord_address = models.CharField(max_length=30, verbose_name="协议地址位")
    accord_com= models.CharField(max_length=30, verbose_name="协议串口号")
    accord_botelv= models.CharField(default="9600", max_length=30, verbose_name="协议波特率")
    accord_databit= models.SmallIntegerField(default=8, verbose_name="协议数据位")
    accord_stopbit= models.SmallIntegerField(default=1, verbose_name="协议停止位")
    accord_check= models.SmallIntegerField(default=2, choices=PARITY_CHECK_CHOICES, verbose_name="协议奇偶校验")
    accord_timeout= models.CharField(max_length=30, verbose_name="协议响应时间")
    accord_readcycle= models.CharField(max_length=30, verbose_name="协议读取周期")
    accord_cmd= models.CharField(max_length=2000, verbose_name="协议指令列表")
    accord_rule= models.SmallIntegerField(default=0, choices=RULE_CHOICES, verbose_name="协议数据转换公式")

    is_show= models.SmallIntegerField(default=0, choices=SHOW_CHOICES, verbose_name="显示标识" )

    class Meta:
        db_table = 'gateway_modbusrtu_models'
        verbose_name = 'ModBusRtu协议配置模型'
        verbose_name_plural = verbose_name


# 设备模板库 modebus
class EquipmentTemplateRtu(BaseModel):
    '''
    ModeBus Rtu 设备模板库Rtu 表 简称 etr
    '''
    FORMAT_DICT = { "Hex": 0, "Long-int": 1, "IEEE-754": 2}
    FORMAT_CHOICES = (
        (0, "Hex"),
        (1, "Long-int"),
        (2, "IEEE-754")
    )
    etr_name        = models.CharField(max_length=30, verbose_name="模板名称")
    etr_remark      = models.CharField(max_length=30, verbose_name="模板描述")
    etr_accordname  = models.CharField(max_length=30, default="ModeBus-RTU", verbose_name="模板协议名称")
    etr_cmdid       = models.CharField(max_length=30, verbose_name="模板下发设备指令id")
    etr_cmdregister = models.CharField(max_length=30, verbose_name="模板下发设备寄存器地址")
    etr_cmdnumber   = models.CharField(max_length=30, verbose_name="模板下发设备寄存器个数")
    etr_param       = models.CharField(max_length=50, verbose_name="模板返回设备数据的参数名")
    etr_format      = models.SmallIntegerField(default=0, choices=FORMAT_CHOICES, verbose_name="模板返回设备数据格式")
    etr_rule        = models.CharField(max_length=30, verbose_name="模板返回数据计算公式")

    class Meta:
        db_table = 'gateway_equipmenttemplatertu'
        verbose_name = 'ModBusRtu设备模板库'
        verbose_name_plural = verbose_name


