from django.shortcuts import render

# Create your views here.
def show_cek_royalti_artis_sw(request):
    return render(request, "cek-royalti-artis-sw.html")

def show_cek_royalti_label(request):
    return render(request, "cek-royalti-label.html")

def show_lagu_di_album(request):
    return render(request, "daftar-lagu-di-album.html")

def show_kelola_album_artis_sw(request):
    return render(request, "kelola-album-artis-sw.html")

def show_kelola_album_label(request):
    return render(request, "kelola-album-label.html")

def show_create_album(request):
    return render(request, "popup-create-album.html")

def show_create_song(request):
    return render(request, "popup-create-song.html")