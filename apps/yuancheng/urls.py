
from django.conf.urls import include, url
from apps.yuancheng import views
from rest_framework import routers
route = routers.DefaultRouter()



# 注册新的路由地址
route.register(r'delivery', views.GateWaySetting)


app_name = 'apps.yuancheng'
urlpatterns = [
    url(r'^manage', views.YuanchengManageView.as_view(), name='yuanchengmanage'),  #
    url(r'^config', views.YuanchengConfigView.as_view(), name='yuanchengconfig'),  #
    url(r'^remote', views.YuanchengRemoteView.as_view(), name='yuanchengremote'),  #
    url('', include(route.urls)),
    url(r'^getlog',views.get_log, name="getlog"),
]