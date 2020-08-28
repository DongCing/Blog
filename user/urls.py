from django.urls import path

from user import views


app_name = 'user'
urlpatterns = [
    path('register', views.user_register, name='register'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),

    path('codelogin', views.code_login, name='codelogin'),
    path('send_code', views.send_code, name='send_code'),

    path('forget_pwd', views.forget_password, name='forget_pwd'),
    path('valide_code', views.valide_code, name='valide_code'),
    # path('update_pwd', update_pwd, name='update_pwd'),
    # path('center', user_center, name='center'),  # 本地存储
    # path('center1', user_center1, name='center1'),  # 云存储
    # path('test', test, name='test'),
]
