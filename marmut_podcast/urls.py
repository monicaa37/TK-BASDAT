from django.urls import path
from marmut_podcast.views import *

app_name = 'marmut_podcast'

urlpatterns = [
    path('chart-detail/<str:type>/', chart_detail, name='chart_detail'),
    path('create-episode', show_create_episode, name='show_create_episode'),
    path('create-podcast', show_create_podcast, name='show_create_podcast'),
    path('list-episode-podcast', show_list_episode_podcast, name='show_list_episode_podcast'),
    path('list-podcast/', show_list_podcast, name='show_list_podcast'),
    path('play-podcast/', play_podcast, name='play_podcast'),
    path('top-charts', show_top_charts, name='show_top_charts'),
]