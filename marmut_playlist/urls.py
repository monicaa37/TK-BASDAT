from django.urls import path
from marmut_playlist.views import show_main, show_form_tambah_playlist
from marmut_playlist.views import tambah_playlist, hapus_playlist, ubah_playlist, playlist_detail
from marmut_playlist.views import shuffle_play, show_play_user_playlist, show_detail_song

app_name = 'marmut_playlist'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('form_tambah_playlist', show_form_tambah_playlist, name='form_tambah_playlist'),
    path('tambah_playlist/', tambah_playlist, name='tambah_playlist'),
    path('hapus_playlist/<int:playlist_id>/', hapus_playlist, name='hapus_playlist'),
    path('ubah_playlist/<int:playlist_id>/', ubah_playlist, name='ubah_playlist'),
    path('playlist/<uuid:playlist_id>/', playlist_detail, name='playlist_detail'),
    path('playlist/<uuid:playlist_id>/shuffle/', shuffle_play, name='shuffle_play'),
    path('play-user-playlist', show_play_user_playlist, name='play-user-playlist'),
    path('detail-song', show_detail_song, name='detail-song'),

]