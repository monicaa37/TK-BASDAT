from django.urls import path
from marmut_playlist.views import show_main, show_form_tambah_playlist
from marmut_playlist.views import tambah_playlist, get_playlist_detail
from marmut_playlist.views import show_play_user_playlist, show_detail_song, show_kelola_playlist

app_name = 'marmut_playlist'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('kelola-playlist', show_kelola_playlist, name='kelola-playlist'),
    path('form-tambah-playlist', show_form_tambah_playlist, name='form-tambah-playlist'),
    path('tambah_playlist/', tambah_playlist, name='tambah_playlist'),
    path('detail-playlist/<uuid:playlist_id>/', get_playlist_detail, name='playlist_detail'),
    path('play-user-playlist/<uuid:playlist_id>/', show_play_user_playlist, name='play-user-playlist'),
    path('detail-song/<uuid:id_konten>/', show_detail_song, name='detail-song'),

]