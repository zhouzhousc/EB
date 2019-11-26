"""edgebox_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.user.views import LoginView
from apps.shebei.views import DeviceView
from django.contrib.auth.decorators import login_required

name="main"
urlpatterns = [

    path('apidata/',include('apps.apidata.urls', namespace='apidata')),
    path('admin/', admin.site.urls),
    # path('search/', include('haystack.urls')),  # 全文检索框架
    path('user/', include('apps.user.urls', namespace='user')),  # 用户登录注册模块
    path('wangguang/', include('apps.wangguang.urls', namespace='wangguang')),  # 网关管理模块
    path('m5/', include('apps.m5.urls', namespace='m5')),  # m5扩展模块
    path('shebei/', include('apps.shebei.urls', namespace='shebei')),  # 设备管理模块
    path('yuancheng/', include('apps.yuancheng.urls', namespace='yuancheng')),  # 远程管理模块
    path('loginfo/', include('apps.loginfo.urls', namespace='loginfo')),  # 日志管理模块
    path('qudong/', include('apps.qudong.urls', namespace='qudong')),  # 驱动管理模块
    path('login/', LoginView.as_view(), name="login"),  # 登录页面
    path('accounts/login/', LoginView.as_view(), name="login"),  # 登录页面
    path('', LoginView.as_view()),  # 登录页面
    path('index/', login_required(DeviceView.as_view()), name="index"),  # 主页(登录验证)
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]