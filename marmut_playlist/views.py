from django.shortcuts import render
# views.py
from django.shortcuts import render, redirect
from .forms import TambahPlaylistForm
from django.utils import timezone
from uuid import UUID
from django.db import connection
from django.shortcuts import render

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
    playlist_detail = {}
    songs = []

    try:
        with connection.cursor() as cursor:
            # Query for playlist details
            cursor.execute("""
                SELECT
                    UP.judul AS playlist_title,
                    AK.nama AS creator,
                    UP.jumlah_lagu AS song_count,
                    CONCAT(UP.total_durasi, ' menit') AS total_duration,
                    TO_CHAR(UP.tanggal_dibuat, 'DD/MM/YYYY') AS created_date,
                    UP.deskripsi AS description
                FROM
                    USER_PLAYLIST UP
                JOIN
                    AKUN AK ON UP.email_pembuat = AK.email
                WHERE
                    UP.id_user_playlist = %s;
            """, [playlist_id])
            playlist_detail_result = cursor.fetchone()
            if playlist_detail_result:
                playlist_detail = {
                    'judul': playlist_detail_result[0],
                    'pembuat': playlist_detail_result[1],
                    'jumlah_lagu': playlist_detail_result[2],
                    'total_durasi': playlist_detail_result[3],
                    'tanggal_dibuat': playlist_detail_result[4],
                    'deskripsi': playlist_detail_result[5]
                }

            # Query for songs in the playlist
            cursor.execute("""
                SELECT
                    KONTEN.judul AS song_title,
                    ARTIST.nama AS artist_name,
                    CONCAT(KONTEN.durasi, ' menit') AS duration
                FROM
                    PLAYLIST_SONG PS
                JOIN
                    SONG S ON PS.id_song = S.id_konten
                JOIN
                    KONTEN ON S.id_konten = KONTEN.id
                JOIN
                    ARTIST ON S.id_artist = ARTIST.id
                WHERE
                    PS.id_playlist = %s;
            """, [playlist_id])
            songs_results = cursor.fetchall()
            for song_result in songs_results:
                song = {
                    'judul': song_result[0],
                    'oleh': song_result[1],
                    'durasi': song_result[2]
                }
                songs.append(song)

    except Exception as e:
        print("Error:", e)
        playlist_detail = {}
        songs = []
    print("halo")
    context = {
        "playlist_detail": playlist_detail,
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


