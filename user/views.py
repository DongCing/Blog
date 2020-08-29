from captcha.models import CaptchaStore
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.handlers.modwsgi import check_password
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from user.forms import UserRegisterForm, RegisterForm, LoginForm, CaptchaTestForm
from user.models import UserProfile
from user.utils import util_sendmsg, send_email


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


# 手机验证码登录
def code_login(request):
    if request.method == 'GET':
        return render(request, 'user/codelogin.html')
    else:
        # 获取表单中填写的验证码和手机号
        mobile = request.POST.get('mobile')
        code = request.POST.get('code')

        # 根据mobile去session中获取服务端验证码
        check_code = request.session.get(mobile)
        if code == check_code:
            user = UserProfile.objects.filter(mobile=mobile).first()
            # user = authenticate(username=user.username, password=user.password)
            print(user)
            if user:
                login(request, user)
                return redirect(reverse('index'))
            else:
                return HttpResponse('验证失败！')
        else:
            return render(request, 'user/codelogin.html', context={'msg': '验证码有误！'})


# 发送验证码路由  ajax发过来的请求
def send_code(request):
    mobile = request.GET.get('mobile')
    data = {}
    if UserProfile.objects.filter(mobile=mobile).exists():
        # 发送验证码  第三方
        json_result = util_sendmsg(mobile)
        # 取值(获取状态码)：
        status = json_result.get('code')
        if status == 200:
            # 获取验证码
            check_code = json_result.get('obj')
            # 使用session保存, key号码
            request.session[mobile] = check_code

            data['status'] = 200
            data['msg'] = '验证码发送成功'
        else:
            data['status'] = 500
            data['msg'] = '验证码发送失败'
    else:
        data['status'] = 501
        data['msg'] = '用户不存在'

    return JsonResponse(data)


# 忘记密码
def forget_password(request):
    if request.method == 'GET':
        form = CaptchaTestForm()
        return render(request, 'user/forget_pwd.html', context={'form': form})
    else:
        # 获取提交的邮箱，发送邮件，通过发送的邮箱链接设置新的密码
        email = request.POST.get('email')
        # 给此邮箱地址发送邮件
        result = send_email(email, request)
        if result:
            return HttpResponse("邮件发送成功！赶快去邮箱更改密码！<a href='/'>返回首页>>> </a>")


# 更新密码,对应找回密码邮件里的url
def update_pwd(request):
    if request.method == 'GET':
        # 点击邮箱中的重置密码链接,获取链接中的 c 参数,即user id对应的随机数
        c = request.GET.get('c')
        # 做为隐藏表单域传递到HTML中
        return render(request, 'user/update_pwd.html', context={'c': c})
    else:
        # 根据提交的表单信息,获取  name = code 的表单信息,即user id对应的随机数
        code = request.POST.get('code')
        # 根据该随机数,即session中的key,获取session中的user id
        uid = request.session.get(code)
        # 获取用户对象
        user = UserProfile.objects.get(pk=uid)
        # 获取密表单中的两个输入密码
        pwd = request.POST.get('password')
        repwd = request.POST.get('repassword')
        if pwd == repwd and user:
            # 将输入的密码加密
            pwd = make_password(pwd)
            # 保存新密码
            user.password = pwd
            user.save()
            return render(request, 'user/update_pwd.html', context={'msg': '用户密码更新成功！'})
        else:
            return render(request, 'user/update_pwd.html', context={'msg': '更新失败！'})


# 定义一个路由验证验证码
def validate_code(request):
    # 判断请求是否是ajax
    if request.is_ajax():
        key = request.GET.get('key')
        code = request.GET.get('code')

        captche = CaptchaStore.objects.filter(hashkey=key).first()
        # response是验证码数据库captcha_captstore中的小写验证码
        if captche.response == code.lower():
            # 正确
            data = {'status': 1}
        else:
            # 错误的
            data = {'status': 0}
        return JsonResponse(data)
