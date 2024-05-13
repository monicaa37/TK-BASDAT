from django.urls import path
from marmut_podcast.views import show_chart_details,show_create_episode,show_create_podcast,show_list_episode_podcast,show_list_podcast,show_play_podcast,show_top_charts

app_name = 'marmut_podcast'

urlpatterns = [
    path('chart-detail', show_chart_details, name='show_chart_details'),
    path('create-episode', show_create_episode, name='show_create_episode'),
    path('create-podcast', show_create_podcast, name='show_create_podcast'),
    path('list-episode-podcast', show_list_episode_podcast, name='show_list_episode_podcast'),
    path('list-podcast', show_list_podcast, name='show_list_podcast'),
    path('play-podcast', show_play_podcast, name='show_play_podcast'),
    path('top-charts', show_top_charts, name='show_top_charts'),
]