
from django.urls import path, include
from django.conf.urls import url
from apps.loginfo import views
from django.conf.urls import include, url
from rest_framework import routers


# 定义路由地址
route = routers.DefaultRouter()
# Log_list_route = routers.DefaultRouter()
NoticeManager_route = routers.DefaultRouter()

# 注册新的路由地址
route.register(r'Event_list', views.EventViewSet)
# Log_list_route.register(r'Log_list', views.LogViewSet)
NoticeManager_route.register(r'NoticeManager', views.NoticeManagerViewSet)


app_name = 'apps.loginfo'
urlpatterns = [
    url(r'^manage', views.LoginfoManageView.as_view(), name='loginfomanage'),  #
    url(r'^log', views.LoginfoLoggerView.as_view(), name='loginfolog'),  #
    url(r'^event', views.LoginfoEventView.as_view(), name='loginfoevent'),  #
    url(r'^notice', views.LoginfoNoticeView.as_view(), name='loginfonotice'),  #
    url(r'^delete', views.NoticeManageDeleteApi.as_view(), name='devicedelete'),  # 单个设备删除
    url('', include(route.urls)),
    # url('', include(Log_list_route.urls)),
    url('', include(NoticeManager_route.urls)),
    url(r'^get_name',views.get_name),
    url(r'^getlog',views.get_log, name="getlog"),
    url(r'^edgebox', views.getlispic, name="edgebox")

]

