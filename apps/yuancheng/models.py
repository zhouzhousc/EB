from django.db import models
from db.base_model import BaseModel

# Create your models here.


class GateWayStatusPub(BaseModel):
    '''网关状态发布模型类'''
    pub_type= models.CharField(max_length=30, verbose_name="发布类型")
    pub_topic= models.CharField(max_length=100, verbose_name="发布主题")
    pub_remark= models.CharField(max_length=100, verbose_name="主题描述")
    pub_num= models.IntegerField(verbose_name="回应次数")

    class Meta:
        db_table = 'gateway_status_pub'
        verbose_name = '网关远程状态发布统计'
        verbose_name_plural = verbose_name

class GateWaySettingDown(BaseModel):
    '''网关远程配置模型类'''
    down_type= models.CharField(max_length=30, verbose_name="下发类型")
    down_topic= models.CharField(max_length=100, verbose_name="下发主题")
    down_remark= models.CharField(max_length=100, verbose_name="主题描述")
    down_num= models.IntegerField(verbose_name="下发次数")

    def __unicode__(self):
        return self.down_type

    class Meta:
        db_table = 'gateway_setting_down'
        verbose_name = '网关远程配置统计'
        verbose_name_plural = verbose_name