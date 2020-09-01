from django import forms
from article.models import Article


# 页面中配置富文本
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        exclude = ['click_num', 'love_num', 'user']
