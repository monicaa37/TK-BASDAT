from django.shortcuts import render
# views.py
from django.shortcuts import render, redirect
from .forms import TambahPlaylistForm
from django.utils import timezone
from uuid import UUID
from django.db import connection

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
            return redirect('kelola_playlist')
    else:
        form = TambahPlaylistForm()

    return render(request, 'kelola_playlist.html', {'form': form})

def tambah_playlist(request):
    if request.method == 'POST':
        # Proses form jika POST request diterima
        # Misalnya, validasi dan penyimpanan data
        return redirect('marmut_playlist:kelola_playlist')
    else:
        # Jika bukan POST request, tampilkan form kosong
        return render(request, 'tambah_playlist.html')

def hapus_playlist(request, playlist_id):
    # Proses penghapusan playlist
    return redirect('marmut_playlist:kelola_playlist')

def ubah_playlist(request, playlist_id):
    if request.method == 'POST':
        # Proses form jika POST request diterima
        # Misalnya, validasi dan penyimpanan data
        return redirect('marmut_playlist:kelola_playlist')
    else:
        # Jika bukan POST request, tampilkan form dengan data playlist
        playlist = {'judul': 'Playlist1', 'deskripsi': 'Deskripsi Playlist1'}
        return render(request, 'ubah_playlist.html', {'playlist': playlist})
    
def get_playlist_detail(playlist_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT up.judul, a.nama, up.jumlah_lagu, up.total_durasi, up.tanggal_dibuat, up.deskripsi
            FROM user_playlist up
            JOIN akun a ON up.email_pembuat = a.email
            WHERE up.id_user_playlist = %s
        """, [playlist_id])
        playlist = cursor.fetchone()

        cursor.execute("""
            SELECT s.judul, a.nama, s.durasi
            FROM playlist_song ps
            JOIN song s ON ps.id_song = s.id_konten
            JOIN artist a ON s.id_artist = a.id
            WHERE ps.id_playlist = (
                SELECT id_playlist FROM user_playlist WHERE id_user_playlist = %s
            )
        """, [playlist_id])
        songs = cursor.fetchall()
    
    return playlist, songs

def format_duration(total_minutes):
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours} jam {minutes} menit"

def playlist_detail(request, playlist_id):
    playlist, songs = get_playlist_detail(playlist_id)
    
    context = {
        'playlist_id': playlist_id,
        'playlist': {
            'judul': playlist[0],
            'pembuat': playlist[1],
            'jumlah_lagu': playlist[2],
            'total_durasi': format_duration(playlist[3]),
            'tanggal_dibuat': playlist[4].strftime('%d/%m/%y'),
            'deskripsi': playlist[5],
        },
        'songs': [
            {'judul': song[0], 'oleh': song[1], 'durasi': format_duration(song[2])}
            for song in songs
        ]
    }
    return render(request, 'play_user_detail.html', context)

def shuffle_play(request, playlist_id):
    current_time = timezone.now()
    user_email = request.COOKIES.get('email')
    
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO akun_play_user_playlist (email_pemain, id_user_playlist, email_pembuat, waktu)
            VALUES (%s, %s, (SELECT email_pembuat FROM user_playlist WHERE id_user_playlist = %s), %s)
        """, [user_email, playlist_id, playlist_id, current_time])

        cursor.execute("""
            SELECT ps.id_song FROM playlist_song ps
            JOIN user_playlist up ON ps.id_playlist = up.id_playlist
            WHERE up.id_user_playlist = %s
        """, [playlist_id])
        song_ids = cursor.fetchall()
        
        for song_id in song_ids:
            cursor.execute("""
                INSERT INTO akun_play_song (email_pemain, id_song, waktu)
                VALUES (%s, %s, %s)
            """, [user_email, song_id[0], current_time])

    return redirect('playlist_detail', playlist_id=playlist_id)