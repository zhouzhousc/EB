
from django.conf.urls import url
# from user import views
from apps.user import views

# app_name = 'user'
app_name = 'apps.user'
urlpatterns = [
    url(r'register/$', views.RegisterView.as_view(), name='register'),  # 注册页面
    url(r'^active/(?P<token>.*)$', views.ActiveView.as_view(), name='active'),  # 用户激活
]
