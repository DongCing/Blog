import xadmin
from article.models import Article, Tag


# 文章管理
class ArticleAdmin(object):
    # 页面中显示的列
    list_display = ['title', 'click_num', 'love_num', 'user']
    # 搜索
    search_fields = ['title', 'id']
    # 可编辑的列
    list_editable = ['click_num', 'love_num']
    # 用于过滤
    list_filter = ['date', 'user']


# 注册
xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(Tag)
