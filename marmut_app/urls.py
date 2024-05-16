from django.urls import path
from marmut_app.views import *

app_name = 'marmut_app'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('pengguna-biasa', show_dashboard_pengguna_biasa, name='show_dashboard_pengguna_biasa'),
    path('artis-sw', show_dashboard_artis_sw, name='show_dashboard_artis_sw'),
    path('label', show_dashboard_label, name='show_dashboard_label'),
    path('pengguna-premium', show_dashboard_pengguna_premium, name='show_dashboard_pengguna_premium'),
    path('podcaster', show_dashboard_podcaster, name="show_dashboard_podcaster"),
    path('dashboard', show_dashboard, name="show_dashboard"),
    path('registration-page', show_registerpage, name="show_registerpage"),
    path('user-regist', show_user_regist, name="show_user_regist"),
    path('label-regist', show_label_regist, name="show_label_regist"),
]