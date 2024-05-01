from django.urls import path
from marmut_app.views import show_main

app_name = 'marmut_app'

urlpatterns = [
    path('', show_main, name='show_main'),
]