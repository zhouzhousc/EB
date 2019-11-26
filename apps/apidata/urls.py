
from django.conf.urls import url, include
# from apidata import views
from apps.apidata import views
from rest_framework.routers import DefaultRouter


# 第一步注册主路由
router = DefaultRouter()
router.register('subdevices', views.SubDeviceViewSet, base_name="subdevice")
router.register('collectdatas', views.CollectDataViewSet, base_name="collectdata")
# router.register('m5collectdatas', views.M5DataViewSet, base_name="m5data")



# app_name = 'apidata'
app_name = 'apps.apidata'
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^m5/notsend/(?P<m5device_name>\d+)/(?P<message_id>\d+)$', views.M5DataListForDevice.as_view(), name='updatem5datafordevice'),
    url(r'^m5/send/(?P<m5device_name>\w+)$', views.M5DataListUpdate.as_view(), name='sendm5datafordevice'),
    url(r'^m5/notsend/(?P<m5device_name>\w+)$', views.M5DataListForDevice.as_view(), name='notsendm5datafordevice'),
    url(r'^m5$', views.M5DataList.as_view(), name='m5data'),
    url(r'^all$', views.DataList.as_view(), name='alldata'),
    url(r'^notsend/(?P<subdevice_id>\d+)$', views.DataListForDevice.as_view(), name='notsenddatafordevice'),
    url(r'^notsend/(?P<subdevice_id>\d+)/(?P<message_id>\d+)$', views.DataListForDevice.as_view(), name='updatedatafordevice'),
    url(r'^send/(?P<subdevice_id>\d+)$', views.DataListUpdate.as_view(), name='senddatafordevice'),

]
