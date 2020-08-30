from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

login_list = ['/user/center', ]


class MiddleWare1(MiddlewareMixin):
    # 重写方法
    # 处理的是request请求
    def process_request(self, request):

        # request 对象就是 view function 函数的 request
        # 获取请求的路径
        path = request.path
        if path in login_list:
            # print(request.user)  # AnonymousUser  匿名用户,未登录
            # print(type(request.user))
            # print(request.user.username)  # 认为就是用户登录的对象
            # 取出当前的对象,判断是否是认证过的
            if not request.user.is_authenticated:
                return redirect(reverse('user:login'))

    # 进入view之前调用的函数
    def process_view(self, request, callback, callback_args, callback_kwargs):
        print('callback_args:', callback_args)
        print('callback_kwargs:', callback_kwargs)
        print('------------->view', callback)
        # callback(request,callback_args,callback_kwargs)

    # render(request,'xxx.html')
    def process_template_response(self):
        pass

    def process_exception(self, request, exception):
        pass

    # 处理的是响应
    def process_response(self, request, response):
        print('==============>response')
        return response


class MiddleWare2(MiddlewareMixin):
    # 重写方法
    def process_request(self, request):
        print('------------->2')
