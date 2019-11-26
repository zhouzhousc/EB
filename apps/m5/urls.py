
from django.conf.urls import url
# from wangguang import views
from apps.m5 import views

app_name = 'apps.m5'
urlpatterns = [
    url(r'^manage$', views.M5ManageView.as_view(), name='m5manage'),  # 注册页面
    url(r'^manage/(?P<m5device_name>\w+)$', views.M5DeviceManageView.as_view(), name='devicemanage'),  # 单个设备管理页面
    url(r'^manage/devicedebug/(?P<m5device_name>\w+)$', views.M5DeviceDebugView.as_view(), name='devicededug'),  # 单个设备管理页面
    url(r'^manage/devicedataforward/(?P<m5device_name>\w+)$', views.M5DeviceDataView.as_view(), name='devicedataforward'),  # 单个设备管理页面

]
