from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.handlers.modwsgi import check_password
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from user.forms import UserRegisterForm, RegisterForm, LoginForm
from user.models import UserProfile


def index(request):
    return render(request, 'index.html')


# 注册
def user_register(request):

    if request.method == 'GET':
        return render(request, 'user/register.html')

    else:
        rform = RegisterForm(request.POST)  # 使用form获取数据
        if rform.is_valid():  # 进行数据的校验
            # 从干净的数据中取值
            username = rform.cleaned_data.get('username')
            email = rform.cleaned_data.get('email')
            mobile = rform.cleaned_data.get('mobile')
            password = rform.cleaned_data.get('password')
            if not UserProfile.objects.filter(Q(username=username) | Q(mobile=mobile)).exists():
                # 注册到数据库中
                password = make_password(password)  # 密码加密
                user = UserProfile.objects.create(username=username, password=password, email=email, mobile=mobile)
                if user:
                    # 注册成功,这里返回登录页面!!
                    return render(request, 'user/login.html')
            else:
                return render(request, 'user/register.html', context={'msg': '用户名或者手机号码已经存在！'})
        return render(request, 'user/register.html', context={'msg': '注册失败，重新填写！'})


# 用户登录
def user_login(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')
    else:
        # 从 LoginForm 中获取提交的数据
        lform = LoginForm(request.POST)
        if lform.is_valid():
            username = lform.cleaned_data.get('username')
            password = lform.cleaned_data.get('password')

            # 方式一:进行数据库的查询,验证密码
            # user = UserProfile.objects.filter(username=username).first()
            # flag = user.check_password(password)
            # if flag:
            #     # 保存session信息
            #     request.session['username'] = username

            # 方式二:前提是继承了AbstractUser
            user = authenticate(username=username, password=password)
            if user:
                # 将用户对象保存在底层的request中 （session）
                login(request, user)

                return redirect(reverse('index'))
        return render(request, 'user/login.html', context={'errors': lform.errors})


# 用户注销
def user_logout(request):
    # request.session.clear()  # 删除字典
    # request.session.flush()  # 删除django_session + cookie +字典
    logout(request)   # django 自带的退出函数

    return redirect(reverse('index'))
