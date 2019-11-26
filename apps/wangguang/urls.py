
from django.conf.urls import url, include
# from wangguang import views
from apps.wangguang import views
from rest_framework import routers


route = routers.DefaultRouter()

route.register(r'SysInfo', views.SysInfoViewSet)

# app_name = 'wangguang'
app_name = 'apps.wangguang'
urlpatterns = [
    url(r'^manage$', views.GatewayManageView.as_view(), name='gatewaymanage'),  # 注册页面
    url(r'^info$', views.GatewayInfoView.as_view(), name='gatewayinfo'),  # 注册页面
    url(r'^sysinfo$', views.GatewaySysInfoView.as_view(), name='gatewaysysinfo'),  # 注册页面
    url(r'^service$', views.GatewayServiceView.as_view(), name='gatewayservice'),  # 注册页面
    url(r'^database', views.getlispic, name="database"),
]
