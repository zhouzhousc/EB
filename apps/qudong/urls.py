
from django.urls import path, include
from django.conf.urls import url
from apps.qudong import views

app_name = 'apps.qudong'
urlpatterns = [
    url(r'^manage', views.QudongManageView.as_view(), name='qudongmanage'),  #
    url(r'^drive', views.QudongDriveView.as_view(), name='qudongdrive'),  #
    url(r'^template', views.QudongTemplateView.as_view(), name='qudongtemplate'),  #

]
