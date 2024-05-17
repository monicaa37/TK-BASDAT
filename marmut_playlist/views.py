from django.shortcuts import render
# views.py
from django.shortcuts import render, redirect
from .forms import TambahPlaylistForm
from django.utils import timezone
from uuid import UUID
from django.db import connection
from django.shortcuts import render, get_object_or_404

# Create your views here.
def show_main(request):
    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A'
    }

    return render(request, "main.html", context)

def show_form_tambah_playlist(request):
    if request.method == 'POST':
        form = TambahPlaylistForm(request.POST)
        if form.is_valid():
            # Ambil data dari form
            judul = form.cleaned_data['judul']
            deskripsi = form.cleaned_data['deskripsi']
            
            # Simpan playlist ke database atau lakukan operasi lainnya sesuai kebutuhan
            # contoh:
            # playlist = Playlist.objects.create(judul=judul, deskripsi=deskripsi)

            # Redirect ke halaman lain setelah menyimpan playlist
            return redirect('marmut_playlist:kelola-playlist')
    else:
        form = TambahPlaylistForm()

    return render(request, 'form_tambah_playlist.html', {'form': form})

def tambah_playlist(request):
    if request.method == 'POST':
        # Proses form jika POST request diterima
        # Misalnya, validasi dan penyimpanan data
        return redirect('marmut_playlist:kelola_playlist')
    else:
        # Jika bukan POST request, tampilkan form kosong
        return render(request, 'tambah_playlist.html')


    
def get_playlist_detail(request):
     return render(request, "play_user_playlist.html")

from django.db import connection
from django.shortcuts import render

def show_play_user_playlist(request):
    query = """
        SELECT 
            K.judul AS "Judul Lagu",
            AK.nama AS "Oleh",
            K.tanggal_rilis AS "Tanggal Rilis",
            COUNT(APS.id_song) AS "Total Plays"
        FROM 
            SONG S
        JOIN 
            KONTEN K ON S.id_konten = K.id
        JOIN 
            ARTIST A ON S.id_artist = A.id
        JOIN 
            AKUN AK ON A.email_akun = AK.email
        JOIN 
            AKUN_PLAY_SONG APS ON S.id_konten = APS.id_song
        GROUP BY
            K.judul, AK.nama, K.tanggal_rilis;
    """

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            chart_data = cursor.fetchall()
            
    except Exception as e:
        print("Error:", e)

    return render(request, "play_user_playlist.html")

def show_detail_song(request):
    return render(request, "tambah_lagu_ke_playlist.html")

def show_kelola_playlist(request):
    return render(request, "kelola_playlist.html")
