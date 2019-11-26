import re
# from user.models import User
from apps.user.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.urls import reverse
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
# from celery_tasks.tasks import send_register_active_email
from .tasks import Send_register_email_tasks
# Create your views here.

# /user/login
class LoginView(View):
    '''登录'''
    def get(self,request):
        #显示登录页面
        return render(request, 'login.html')

    def post(self,request):

        #接收数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        #校验收据
        if not all([username, password]):
            return render(request, 'login.html', {"errmsg": "用户名和密码不能为空"})
        #业务处理：登录校验
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user) # 登录并记录用户的登录状态
                # 获取登录后所要跳转到的地址, 默认跳转首页
                next_url = request.GET.get('next', reverse('index'))
                #  跳转到next_url
                response = redirect(next_url)  # HttpResponseRedirect
                return response
            else:
                # print("The passwoed is valid, but the account has been disabled!")
                return render(request, 'login.html', {'errmsg': '账户未激活'})
        else:
            return render(request, 'login.html', {'errmsg': '用户名或密码错误'})

# /user/register
class RegisterView(View):
    '''注册类'''
    def get(self, request):
        # 显示注册页面
        return render(request, 'register.html')

    def post(self, request):
        # 进行注册处理
        # 接收数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        # 进行数据校验
        if not all([username, password, email]):
            # 数据不完整
            return render(request, 'register.html', {'errmsg': '用户名、邮箱、密码不能为空'})
        # 检验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,8}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})
        # 校验用户是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None
        if user:
            return render(request, 'register.html', {'errmsg': '用户已存在'})
        # 业务处理：进行用户注册
        user = User.objects.create_user(username, email, password)
        user.is_active = 0 #1不用激活链接、0需要激活连接
        user.save()

        # 发送激活链接，包含激活链接：http://127.0.0.1:8000/user/active/5
        # 激活链接中需要包含用户的身份信息，并要把身份信息进行加密
        # 激活链接格式: /user/active/用户身份加密后的信息 /user/active/token

        # 加密用户的身份信息，生成激活token
        serializer = Serializer(settings.SECRET_KEY, 3600*2)
        info = {'confirm': user.id}
        token = serializer.dumps(info)  # bytes
        token = token.decode('utf8')  # 解码, str

        # 发邮箱
        subject = 'Edge Box 账户激活链接 '+"<用户名:"+username+">"
        receiver = email
        html_message = '%s, 你好！\n' \
                       '请于2h内点击下面链接激活您的账户' \
                       'http://127.0.0.1:9090/user/active/%s' % (username, token)
        Send_register_email_tasks.delay(receiver, subject, html_message)
        # 返回应答,跳转登录页
        return redirect(reverse('login'))

# /user/active/加密信息token
class ActiveView(View):
    """用户激活"""
    def get(self, request, token):
        # 进行用户激活
        # 进行解密，获取要激活的用户信息
        serializer = Serializer(settings.SECRET_KEY, 3600*2)
        try:
            info = serializer.loads(token)
            # 获取待激活用户的id
            user_id = info['confirm']

            # 根据id获取用户信息
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            # 跳转到登录页面
            return redirect(reverse('login'))
        except SignatureExpired as e:
            # 激活链接已过期
            return HttpResponse('激活链接已失效')