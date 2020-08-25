from django.contrib.auth.models import AbstractUser
from django.db import models


# 继承Django内置的用户表,并添加新的字段
class UserProfile(AbstractUser):
    # verbose_name 就是在后台显示对对应的名称
    mobile = models.CharField(max_length=11, verbose_name='手机号码', unique=True)
    icon = models.ImageField(upload_to='uploads/%Y/%m/%d/', default="")

    class Meta:
        db_table = 'userprofile'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
