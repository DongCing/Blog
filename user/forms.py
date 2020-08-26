import re

from django import forms
from django.core.exceptions import ValidationError
from django.forms import Form


class UserRegisterForm(Form):
    username = forms.CharField(max_length=50, min_length=6,
                               error_messages={'min_length': '用户名至少六位', },
                               label='用户名:')
    email = forms.EmailField(required=True, error_messages={'required': '必填'},
                             label='邮箱')
    mobile = forms.CharField(required=True, error_messages={'required': '必填'},
                             label='手机')
    # 加上widget插件,输入密码可以隐藏
    password = forms.CharField(required=True, error_messages={'required': '必填'},
                               label='密码', widget=forms.widgets.PasswordInput)
    re_password = forms.CharField(required=True, error_messages={'required': '必填'},
                                  label='确认密码', widget=forms.widgets.PasswordInput)

    # 校验函数
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # 校验正则式,六位密码,字母开头
        result = re.match(r'[a-zA-Z]\w{5,}', username)
        if not result:
            # 校验错误
            raise ValidationError('必须字母开头六位')
        return username
