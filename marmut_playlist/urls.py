from django.urls import path
from marmut_playlist.views import show_main

app_name = 'marmut_playlist'

urlpatterns = [
    path('', show_main, name='show_main'),
]