
from django.conf.urls import url
# from shebei import views
from apps.shebei import views

# app_name = 'shebei'
app_name = 'apps.shebei'
urlpatterns = [
    url(r'^devicelist$', views.DeviceListView.as_view(), name='devicelist'),  # 设备列表页面
    url(r'^devicemanage/(?P<device_id>\d+)$', views.DeviceManageView.as_view(), name='devicemanage'),  # 单个设备管理页面
    url(r'^devicemanage/deviceinfo/(?P<device_id>\d+)$', views.DeviceInfoView.as_view(), name='deviceinfo'),  # 单个设备基本信息页面
    url(r'^devicemanage/deviceprotocol/(?P<device_id>\d+)$', views.DeviceProtocolView.as_view(), name='deviceprotocol'),  # 单个设备协议配置页面
    url(r'^deviceprotocol/apply$', views.DeviceProtocolApi.as_view(), name='modelapply'),  # 单个设备模板应用保存
    url(r'^devicemanage/devicededug/(?P<device_id>\d+)$', views.DeviceDebugView.as_view(), name='devicededug'),  # 单个设备调试页面
    url(r'^devicemanage/devicedataforward/(?P<device_id>\d+)$', views.DeviceDataView.as_view(), name='devicedataforward'),  # 单个设备数据转发页面
    url(r'^delete/', views.DeviceDeleteApi.as_view(), name='devicedelete'),  # 单个设备删除
    url(r'^update$', views.DeviceUpdateApi.as_view(), name='deviceupdate'),  # 单个设备启用禁用更新
    url(r'^transmit/update$', views.TransmitUpdateApi.as_view(), name='transmitupdate'),  # 数据转发更新
    url(r'^transmit/delete$', views.TransmitDeleteApi.as_view(), name='transmitdelete'),  # 数据转发删除
    url(r'^transmit/count$', views.TransmitCountApi.as_view(), name='transmitcount'),  # 数据转发计数
    url(r'^transmit/modify$', views.TransmitModifyApi.as_view(), name='transmitmodify'),  # 数据转发计数
    url(r'^modify/', views.DeviceModifyApi.as_view(), name='devicemodify'),  # 单个设备信息修改页面

]
