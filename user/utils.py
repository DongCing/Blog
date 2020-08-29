# 作用就是向网易云信发送请求，帮助后台发送短信息给客户
import hashlib
import json
import os
import uuid
from time import time

import requests
from django.core.mail import send_mail
# from qiniu import Auth, put_file, put_data
#
# from djangoday4.settings import EMAIL_HOST_USER, MEDIA_ROOT
from blog.settings import EMAIL_HOST_USER
from user.models import UserProfile


# 发送短信息
def util_sendmsg(mobile):
    # 网易云信的请求地址
    url = 'https://api.netease.im/sms/sendcode.action'
    # 通过 mobile 参数获取手机号
    data = {'mobile': mobile}

    # 4部分组成 headers： AppKey  Nonce  CurTime  CheckSum
    AppKey = '1bdcdeda105c1d91e802a191d8f5ed94'
    Nonce = '843hjfd87fdfshdjfhs5433'
    CurTime = str(time())
    AppSecret = '05bf2ece7293'
    content = AppSecret + Nonce + CurTime
    # 加密
    CheckSum = hashlib.sha1(content.encode('utf-8')).hexdigest()

    headers = {'AppKey': AppKey, 'Nonce': Nonce, 'CurTime': CurTime, 'CheckSum': CheckSum}

    # 使用 requests(相当于浏览器) 发送post请求
    response = requests.post(url, data, headers=headers)
    # json
    str_result = response.text  # 获取响应体,json在响应体中

    json_result = json.loads(str_result)  # 转成json

    return json_result


# 发送邮件
def send_email(email, request):
    subject = '个人博客找回密码'
    user = UserProfile.objects.filter(email=email).first()
    # 生成一个随机码,和用户ID绑定保存在session中,根据它找到用户ID
    ran_code = uuid.uuid4()
    # print(ran_code)
    # print(type(ran_code))
    ran_code = str(ran_code)
    # print(type(ran_code))
    ran_code = ran_code.replace('-', '')
    request.session[ran_code] = user.id
    message = '''
     尊敬的用户:
            <br>
            您好！此链接用户找回密码，请点击链接: <a href='http://127.0.0.1:8000/user/update_pwd?c=%s'>更新密码</a>，
            <br>
            如果链接不能点击，请复制：<br>
            http://127.0.0.1:8000/user/update_pwd?c=%s

           个人博客团队
    ''' % (ran_code, ran_code)
    # 发送邮件send_mail
    result = send_mail(subject, "", EMAIL_HOST_USER, [email, ], html_message=message)
    return result


# 上传图片到七牛云
# def upload_image(storeobj):
#     access_key = '1fXvG9wkbN7AgRUG6usHDcRP5Bb85apcovRAIITP'
#     secret_key = 'Aqf1lPAmUG72EdZJ7PxKtWHfWDYNdUycZP1TaAIN'
#
#     # 构建鉴权对象
#     q = Auth(access_key, secret_key)
#
#     # 要上传的空间
#     bucket_name = 'myblog'
#
#     # 上传后保存的文件名
#     key = storeobj.name
#
#     # 生成上传 Token，可以指定过期时间等
#     token = q.upload_token(bucket_name, key, 3600)
#
#     # 要上传文件的本地路径
#     # localfile = os.path.join(MEDIA_ROOT, imagepath)  # 本地图片
#     ret, info = put_data(token, key, storeobj.read())
#
#     print(ret, info)
#     filename = ret.get('key')
#     save_path = 'http://pr67kkhq9.bkt.clouddn.com/' + filename
#     return save_path
