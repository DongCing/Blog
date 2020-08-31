from django.contrib.auth.decorators import login_required
from django.core.checks import Tags
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

# from article.forms import ArticleForm
from article.models import Article, Tag, Comment #Message


# 文章详情
def article_detail(request):
    id = request.GET.get('id')
    article = Article.objects.get(pk=id)
    # 当文章详情有点击时,浏览量 +1
    article.click_num += 1
    article.save()
    # 查询相关文章
    tags_list = article.tags.all()  # 添加（）
    list_about = []  # 存放文章的列表
    for tag in tags_list:
        for article1 in tag.article_set.all():
            if article1 not in list_about and len(list_about) < 6:
                list_about.append(article1)

    # 查询评论数
    comments = Comment.objects.filter(article_id=id)

    return render(request, 'article/info.html',
                  context={'article': article, 'list_about': list_about, 'comments': comments})


# 学无止境 + 分页器
def article_show(request):
    tags = Tag.objects.all()[:6]

    tid = request.GET.get('tid', "")  # None
    if tid:
        tag = Tag.objects.get(pk=tid)
        # articles = tag.article_set.all()
        articles = Article.objects.filter(tags__name=tag.name)
    else:
        articles = Article.objects.all()

    # 分页显示
    paginator = Paginator(articles, 3)  # Paginator(对象列表，每页几条记录)
    print(paginator.count)  # 总的条目数  总的记录数
    print(paginator.num_pages)  # 可以分页的数量  总的页码数
    print(paginator.page_range)  # 页面的范围

    # 方法： get_page()
    page_number = request.GET.get('page', 1)    # 取不到,默认1
    print(page_number)
    page = paginator.get_page(page_number)  # 返回的是page对象
    print('--->', page_number, page.number)
    # page.has_next()  # 有没有下一页
    # page.has_previous()  # 判断是否存在前一页
    # page.next_page_number() # 获取下一页的页码数
    # page.previous_page_number() # 获取前一页的页码数

    # 属性：
    # object_list   当前页的所有对象
    #  number       当前的页码数
    # paginator     分页器对象

    return render(request, 'article/learn.html', context={'page': page, 'tags': tags, 'tid': tid})


# 写博客
# @login_required
# def write_article(request):
#     if request.method == 'GET':
#         aform = ArticleForm()
#         return render(request, 'article/write.html', context={'form': aform})
#     else:
#         aform = ArticleForm(request.POST, request.FILES)
#         if aform.is_valid():
#             data = aform.cleaned_data
#             article = Article()
#             article.title = data.get('title')
#             article.desc = data.get('desc')
#             article.content = data.get('content')
#             print(type(data.get('image')))
#
#             article.image = data.get('image')
#             article.desc = data.get('desc')
#             article.user = request.user  # 1对多 直接赋值
#             article.save()
#
#             # 多对多 必须添加到文章保存的后面添加
#             article.tags.set(data.get('tags'))
#             return redirect(reverse('index'))
#
#         return render(request, 'article/write.html', context={'form': aform})
#
#
# # 文章评论
# def article_comment(request):
#     # 直接接受
#     nickname = request.GET.get('nickname')
#     content = request.GET.get('saytext')
#     aid = request.GET.get('aid')
#
#     comment = Comment.objects.create(nickname=nickname, content=content, article_id=aid)
#
#     if comment:
#         data = {'status': 1}
#     else:
#         data = {'status': 0}
#     return JsonResponse(data)
#
#
# # 留言
# def blog_message(request):
#     messages = Message.objects.all()
#     paginator = Paginator(messages, 8)
#     # 获取页码数
#     page = request.GET.get('page', 1)
#     # 得到page对象
#     page = paginator.get_page(page)
#
#     if request.method == 'GET':
#         return render(request, 'article/lmessage.html', context={'page':page})
#     else:
#         name = request.POST.get('name')
#         mycall = request.POST.get('mycall')
#         lytext = request.POST.get('lytext')
#         if name and lytext:
#             message = Message.objects.create(nickname=name, icon=mycall, content=lytext)
#             if message:
#                 return redirect(reverse('article:message'))
#         return render(request, 'article/lmessage.html', context={'page':page, 'error': '必须输入用户名和内容'})
