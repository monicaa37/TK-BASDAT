from django.shortcuts import render
from django.db import connection

# Create your views here.
def show_cek_royalti_artis_sw(request):
    roles = request.COOKIES.get('role')
    royaltis = []

    try:
        if 'artist' in roles:
            query_artist = """
                SELECT K.judul AS judul_lagu,
                    A.judul AS judul_album,
                    S.total_play AS  total_play,
                    S.total_download AS total_download,
                    (S.total_play * PHC.rate_royalti) AS royalti_didapat
                FROM KONTEN K
                JOIN SONG S ON K.id = S.id_konten
                JOIN ROYALTI R ON S.id_konten = R.id_song
                JOIN ALBUM A ON S.id_album = A.id
                JOIN PEMILIK_HAK_CIPTA PHC ON R.id_pemilik_hak_cipta = PHC.id
                JOIN ARTIST AR on PHC.id = AR.id_pemilik_hak_cipta
                WHERE AR.email_akun = %s"""
            with connection.cursor() as cursor:
                cursor.execute(query_artist, [request.COOKIES.get('email')])
                royalti_artist = cursor.fetchall()
            royaltis.extend(royalti_artist)

        if 'songwriter' in roles:
            print(request.COOKIES.get('email'))
            query_sw = """
                SELECT K.judul AS judul_lagu,
                    A.judul AS judul_album,
                    S.total_play AS  total_play,
                    S.total_download AS total_download,
                    (S.total_play * PHC.rate_royalti) AS royalti_didapat
                FROM KONTEN K
                JOIN SONG S ON K.id = S.id_konten
                JOIN ROYALTI R ON S.id_konten = R.id_song
                JOIN ALBUM A ON S.id_album = A.id
                JOIN PEMILIK_HAK_CIPTA PHC ON R.id_pemilik_hak_cipta = PHC.id
                JOIN SONGWRITER SW on PHC.id = SW.id_pemilik_hak_cipta
                WHERE SW.email_akun = %s"""
            with connection.cursor() as cursor:
                cursor.execute(query_sw, [request.COOKIES.get('email')])
                royalti_sw = cursor.fetchall()
            royaltis.extend(royalti_sw)
    
    except Exception as e:
        print("Error:", e)
        royaltis = []
    return render(request, "cek-royalti-artis-sw.html", {"royaltis": royaltis})


def show_cek_royalti_label(request):
    try:
        query = """
            SELECT K.judul AS judul_lagu,
                A.judul AS judul_album,
                S.total_play AS  total_play,
                S.total_download AS total_download,
                (S.total_play * PHC.rate_royalti) AS royalti_didapat
            FROM KONTEN K
            JOIN SONG S ON K.id = S.id_konten
            JOIN ROYALTI R ON S.id_konten = R.id_song
            JOIN ALBUM A ON S.id_album = A.id
            JOIN PEMILIK_HAK_CIPTA PHC ON R.id_pemilik_hak_cipta = PHC.id
            JOIN LABEL L on PHC.id = L.id_pemilik_hak_cipta
            WHERE L.id = %s"""
        with connection.cursor() as cursor:
            cursor.execute(query, [request.COOKIES.get('id')])
            royaltis = cursor.fetchall()
    except Exception as e:
        print("Error:", e)
        royaltis = []
    return render(request, "cek-royalti-label.html", {"royaltis": royaltis})


def show_lagu_di_album(request):
    return render(request, "daftar-lagu-di-album.html")


def show_kelola_album_artis_sw(request):
    return render(request, 'kelola-album-artis-sw.html')


def show_kelola_album_label(request):
    try:
        albums = []
        query = """
        SELECT A.judul AS "Judul Album",
               A.jumlah_lagu AS "Jumlah Lagu",
               A.total_durasi AS "Total Durasi"
        FROM ALBUM A
        JOIN LABEL L ON A.id_label = L.id
        WHERE L.id = %s"""
        with connection.cursor() as cursor:
            cursor.execute(query, [request.COOKIES.get('id')])
            albums = cursor.fetchall()
    except Exception as e:
        print("Error:", e)
        albums = []
    return render(request, 'kelola-album-label.html', {"albums" : albums})


def show_create_album(request):
    return render(request, "popup-create-album.html")

def show_create_song(request):
    return render(request, "popup-create-song.html")

def test(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM akun")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
    except Exception as e:
        print("Error:", e)

    return render(request, "test.html")