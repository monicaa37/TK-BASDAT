from django.urls import path
from marmut_app.views import show_label_regist, show_main,show_login,show_registerpage, show_user_regist

app_name = 'marmut_app'

urlpatterns = [
    path('main', show_main, name='show_main'),
    path('login', show_login, name='show_login'),
    path('registration-page', show_registerpage, name='show_registerpage'),
    path('label-regist', show_label_regist, name='show_label_regist'),
    path('user-regist', show_user_regist, name='show_user_regist'),
]