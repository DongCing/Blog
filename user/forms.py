import re

from captcha.fields import CaptchaField
from django import forms
from django.core.exceptions import ValidationError
from django.forms import Form, ModelForm, EmailField

from user.models import UserProfile


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

    # 校验函数
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # 校验正则式,六位密码,字母开头
        result = re.match(r'[a-zA-Z]\w{5,}', username)
        if not result:
            # 校验错误
            raise ValidationError('必须字母开头六位')
        return username


# ModelForm 作用同 Form
class RegisterForm(ModelForm):

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'mobile', 'password']
        # 创建所有字段的表单数据
        # fields = '__all__'
        # 排除列表中的字段,创建其余字段的表单数据
        # exclude = ['first_name','date_joined','last_name']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # result = re.match(r'[a-zA-Z]\w{5,}', username)
        # if not result:
        #     raise ValidationError('用户名必须字母开头')
        return username


# 登录校验
class LoginForm(Form):
    username = forms.CharField(max_length=50, min_length=1, error_messages={'min_length': '用户名长度至少1位', }, label='用户名')
    password = forms.CharField(required=True, error_messages={'required': '必须填写密码'}, label='密码',
                               widget=forms.widgets.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not UserProfile.objects.filter(username=username).exists():
            raise ValidationError('用户名不存在')
        return username


# 验证码captcha的Form
class CaptchaTestForm(forms.Form):

    email = EmailField(required=True, error_messages={'required': '必须填写邮箱'}, label='邮箱')
    captcha = CaptchaField()
