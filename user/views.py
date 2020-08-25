from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


# 注册
def register(request):

    if request.method == 'GET':
        return render(request, 'user/register.html')

    else:
        return None
