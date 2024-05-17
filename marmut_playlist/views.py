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

def show_play_user_playlist(request, playlist_id):
    songs = []
    try:
        with connection.cursor() as cursor:
            # Mendapatkan detail lagu
            cursor.execute("""
            SELECT SONG.id_konten, KONTEN.judul, AKUN.nama AS artist, KONTEN.durasi
            FROM PLAYLIST_SONG
            JOIN SONG ON PLAYLIST_SONG.id_song = SONG.id_konten
            JOIN KONTEN ON SONG.id_konten = KONTEN.id
            JOIN ARTIST ON SONG.id_artist = ARTIST.id
            JOIN AKUN ON ARTIST.email_akun = AKUN.email
            WHERE PLAYLIST_SONG.id_playlist = %s
            """, [playlist_id])
            songs_results = cursor.fetchall()
            for song_result in songs_results:
                song = {
                    'id': song_result[0],
                    'judul': song_result[1],
                    'oleh': song_result[2],
                    'total_durasi': song_result[4]
                }
                songs.append(song)
            
    except Exception as e:
        print("Error:", e)
        songs = []
    print("halooo")
    print(songs)
    context = {
        "songs": songs
    }

    return render(request, "play_user_playlist.html", context)








def show_detail_song(request,id_konten):
    query = """
    SELECT 
    k.judul AS "Judul",
    STRING_AGG(DISTINCT g.genre, ', ') AS "Genre(s)",
    a.nama AS "Artist",
    STRING_AGG(DISTINCT sw.nama, ', ') AS "Songwriter(s)",
    k.durasi AS "Durasi",
    k.tanggal_rilis AS "Tanggal Rilis",
    EXTRACT(YEAR FROM k.tanggal_rilis) AS "Tahun",
    al.judul AS "Album"
FROM 
    SONG s
JOIN 
    KONTEN k ON s.id_konten = k.id
JOIN 
    ARTIST a ON s.id_artist = a.id
LEFT JOIN 
    GENRE g ON s.id_konten = g.id_konten
LEFT JOIN 
    SONGWRITER_WRITE_SONG sws ON s.id_konten = sws.id_song
LEFT JOIN 
    SONGWRITER sw ON sws.id_songwriter = sw.id
LEFT JOIN 
    ALBUM al ON s.id_album = al.id
GROUP BY 
    k.judul, a.nama, k.durasi, k.tanggal_rilis, al.judul;

    """
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            song_details = cursor.fetchall()
            song_data = {
                "Judul": song_details[0][0],
                "Genre(s)": song_details[0][1],
                "Artist": song_details[0][2],
                "Songwriter(s)": song_details[0][3],
                "Durasi": song_details[0][4],
                "Tanggal Rilis": song_details[0][5].strftime("%d/%m/%y"),
                "Tahun": song_details[0][6],
                "Album": song_details[0][7]
            }
    except Exception as e:
        print("Error:", e)
        song_data = {}
    print("ini data song") 
    print(song_data)
    return render(request, "tambah_lagu_ke_playlist.html", {"song_data": song_data})










def show_kelola_playlist(request):
    query = """
        SELECT 
            judul AS "Judul",
            jumlah_lagu AS "Jumlah Lagu",
            total_durasi AS "Total Durasi",
            'Action' AS "Action"
        FROM 
            USER_PLAYLIST;
    """

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            chart_data = cursor.fetchall()
        
        # Format data untuk dikirimkan ke template
        formatted_data = [
            {
                "Judul": row[0],
                "Jumlah_Lagu": row[1],
                "Total_Durasi": f"{row[2] // 60} jam {row[2] % 60} menit",
                "Action": row[3]  # Ganti ini dengan tindakan yang sebenarnya seperti tombol atau link
            }
            for row in chart_data
        ]
        
    except Exception as e:
        print("Error:", e)
        formatted_data = []

    return render(request, "kelola_playlist.html", {"playlists": formatted_data})


