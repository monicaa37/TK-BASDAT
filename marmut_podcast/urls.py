from django.urls import path
from marmut_podcast.views import show_main

app_name = ''

urlpatterns = [
    path('', show_main, name='show_main'),
]