from django.urls import path
from marmut_playlist.views import show_main, show_form_tambah_playlist, tambah_playlist, hapus_playlist, ubah_playlist 

app_name = 'marmut_playlist'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('form_tambah_playlist', show_form_tambah_playlist, name='form_tambah_playlist'),
    path('tambah_playlist/', tambah_playlist, name='tambah_playlist'),
    path('hapus_playlist/<int:playlist_id>/', hapus_playlist, name='hapus_playlist'),
    path('ubah_playlist/<int:playlist_id>/', ubah_playlist, name='ubah_playlist'),
    
]