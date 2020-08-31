import xadmin
from user.models import UserProfile


# 后台基本设置
from xadmin import views


class BaseSettings(object):
    # 界面主题设置
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = '博客后台管理'
    site_footer = '小楼昨夜又东风'


# 注册
xadmin.site.register(views.BaseAdminView, BaseSettings)
xadmin.site.register(views.CommAdminView, GlobalSettings)