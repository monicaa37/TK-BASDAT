from django.urls import path
from marmut_app.views import *

app_name = 'marmut_app'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('dashboard', show_dashboard, name="show_dashboard"),
    path('registration-page', show_registerpage, name="show_registerpage"),
    path('user-regist', show_user_regist, name="show_user_regist"),
    path('label-regist', show_label_regist, name="show_label_regist"),
    path('register', register, name='register'),
    path('insert_label', insert_label, name='insert_label'),
]