from django.urls import path
from marmut_album.views import *

app_name = 'marmut_album'

urlpatterns = [
    path('cek-royalti-artis-sw', show_cek_royalti_artis_sw, name="show_cek_royalti_artis_sw"),
    path('cek-royalti-label', show_cek_royalti_label, name="show_cek_royalti_label"),
    path('lagu-di-album/<str:type>', show_lagu_di_album, name="show_lagu_di_album"),
    path('kelola-album-artis-sw', show_kelola_album_artis_sw, name="show_kelola_album_artis_sw"),
    path('kelola-album-label', show_kelola_album_label, name="show_kelola_album_label"),
    path('create-album', show_create_album, name="show_create_album"),
    path('create-song', show_create_song, name="show_create_song"),
    path('delete-album/<type>/', delete_album, name='delete_album'),
    path('insert-album/', insert_album, name='insert_album'),
    path('insert-song/', insert_song, name='insert_song'),
    path('delete-song/<type>/', delete_song, name='delete_song'),
]