from django.http import HttpResponse
from django.shortcuts import render

from user.forms import UserRegisterForm


def index(request):
    return render(request, 'index.html')


# 注册
def register(request):

    if request.method == 'GET':
        return render(request, 'user/register.html')

    else:
        return None


def zhuce(request):
    if request.method == 'GET':
        rform = UserRegisterForm()
        return render(request, 'user/zhuce.html', context={'rform': rform})

    else:
        rform = UserRegisterForm(request.POST)
        # 判断是否符合验证
        print(rform.is_valid())
        # 打印验证出错错误地方
        print(rform.errors)
        return HttpResponse("OK")
