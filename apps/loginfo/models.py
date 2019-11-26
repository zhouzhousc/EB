# -*-coding:utf-8*-
from django.db import models
from db.base_model import BaseModel



class Log_list(BaseModel):
    """日志中心"""
    ENABLE_CHOICES=(
        (0, "未启用"),
        (1, "启用")
    )
    LOG_NAME=(
        (1, "系统日志"),
        (2, "采集日志"),
        (3, "传输日志"),
        (4, "网络日志"),
        (5, "权限日志"),
    )
    # subdevice = models.ForeignKey('shebei.SubDevice', to_field='id', on_delete=models.CASCADE, verbose_name='子设备id')
    log_type = models.CharField(max_length=30, verbose_name="文件名")
    log_leader = models.CharField(max_length=30, verbose_name="管理者")
    log_level = models.CharField(max_length=30, verbose_name="日志级别")
    log_info = models.CharField(max_length=30, verbose_name="描述")
    log_no = models.SmallIntegerField(default=0, choices=LOG_NAME, verbose_name="日志类型")

    # def __unicode__(self):
    #     return '%d: %s' % (self.pk, self.log_leader)
    def __unicode__(self):
        return self.log_no

    class Meta:
        db_table = 'gateway_log_list'
        verbose_name = '日志中心'
        verbose_name_plural = verbose_name

class NoticeManager(BaseModel):
    """通知管理"""
    ENABLE_CHOICES=(
        (0, "未启用"),
        (1, "启用")
    )
    notice_leader = models.CharField(max_length=30, verbose_name="責任人")
    notice_location = models.CharField(max_length=30, verbose_name="地點")
    notice_message_num = models.CharField(max_length=30, verbose_name="消息數據")
    notice_time = models.CharField(max_length=30, verbose_name="時間")
    notice_status = models.CharField(max_length=30, verbose_name="狀態")
    notice_phone = models.CharField(max_length=30, verbose_name="電話")
    notice_email = models.CharField(max_length=50, verbose_name="郵箱")
    # notice_enable = models.SmallIntegerField(default=1, choices=ENABLE_CHOICES, verbose_name="使用者_激活使能")

    def __unicode__(self):
        return '%d: %s' % (self.pk, self.notice_leader)

    class Meta:
        db_table = 'gateway_notice_manager'
        verbose_name = '通知管理'
        verbose_name_plural = verbose_name

class Event_list(BaseModel):
    """事件中心"""
    event_no = models.CharField(max_length=30, verbose_name="序號")
    event_leader = models.CharField(max_length=30, verbose_name="用戶名")
    event_info = models.CharField(max_length=100, verbose_name="事件詳情")
    event_create_time = models.CharField(max_length=30, verbose_name="記錄時間")
    event_type = models.CharField(max_length=30, verbose_name="事件類型")
    # event_status = models.CharField(max_length=30, verbose_name="事件通知狀態")
    # notice_enable = models.SmallIntegerField(default=1, choices=ENABLE_CHOICES, verbose_name="使用者_激活使能")

    def __unicode__(self):
        return '%d: %s' % (self.pk, self.event_no)

    class Meta:
        db_table = 'gateway_event_list'
        verbose_name = '事件中心'
        verbose_name_plural = verbose_name

class Name(BaseModel):
    """事件中心"""
    name = models.CharField(max_length=30, verbose_name="名字")
    age = models.IntegerField()
    # event_info = models.CharField(max_length=100, verbose_name="事件詳情")
    # event_create_time = models.CharField(max_length=30, verbose_name="記錄時間")
    # event_type = models.CharField(max_length=30, verbose_name="事件類型")
    # notice_enable = models.SmallIntegerField(default=1, choices=ENABLE_CHOICES, verbose_name="使用者_激活使能")
    #
    # def __unicode__(self):
    #     return '%d: %s' % (self.pk, self.event_no)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'gateway_name'
        verbose_name = '測試'
        verbose_name_plural = verbose_name

