from django.urls import path
from marmut_app.views import *

app_name = 'marmut_app'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('dashboard', show_dashboard, name="show_dashboard")
]