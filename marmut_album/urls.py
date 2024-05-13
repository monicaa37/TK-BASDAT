from django.urls import path
from marmut_album.views import show_main

app_name = 'marmut_album'

urlpatterns = [
    path('', show_main, name='show_main'),
]