from datetime import date
import uuid
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

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


@csrf_exempt
def show_lagu_di_album(request, type):
    judul_album = type

    query = """
        SELECT K.judul AS "Judul Lagu",
               K.durasi AS "Durasi Lagu",
               S.total_play AS "Total Play",
               S.total_download AS "Total Download",
               K.id AS "ID Lagu"
        FROM KONTEN K
        JOIN SONG S ON K.id = S.id_konten
        JOIN ALBUM A ON S.id_album = A.id
        WHERE A.judul = %s"""
    with connection.cursor() as cursor:
            cursor.execute(query, [judul_album])
            songs = cursor.fetchall()

    return render(request, "daftar-lagu-di-album.html", {"judul_album": judul_album, "songs": songs})


def show_kelola_album_artis_sw(request):
    roles = request.COOKIES.get('role')
    albums = []

    try:
        if 'artist' in roles:
            query_artist = """
                SELECT DISTINCT A.judul AS "Judul Album",
                                L.nama AS "Nama Label",
                                A.jumlah_lagu AS "Jumlah Lagu",
                                A.total_durasi AS "Total Durasi"
                FROM ALBUM A
                JOIN LABEL L ON A.id_label = L.id
                JOIN SONG S ON A.id = S.id_album
                JOIN ARTIST AR ON S.id_artist = AR.id
                WHERE AR.email_akun = %s"""
            with connection.cursor() as cursor:
                cursor.execute(query_artist, [request.COOKIES.get('email')])
                album_artist = cursor.fetchall()
            albums.extend(album_artist)

        if 'songwriter' in roles:
            query_sw = """
                SELECT DISTINCT A.judul AS "Judul Album",
                                L.nama AS "Nama Label",
                                A.jumlah_lagu AS "Jumlah Lagu",
                                A.total_durasi AS "Total Durasi"
                FROM ALBUM A
                JOIN LABEL L ON A.id_label = L.id
                JOIN SONG S ON A.id = S.id_album
                JOIN SONGWRITER SW ON S.id_artist = SW.id
                WHERE SW.email_akun = %s"""
            with connection.cursor() as cursor:
                cursor.execute(query_sw, [request.COOKIES.get('email')])
                album_sw = cursor.fetchall()
            albums.extend(album_sw)
    
    except Exception as e:
        print("Error:", e)
        albums = []
    return render(request, "kelola-album-artis-sw.html", {"albums": albums})


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


@csrf_exempt
def show_create_album(request):
    query = """
    SELECT id, nama
    FROM LABEL"""
    with connection.cursor() as cursor:
        cursor.execute(query)
        labels = cursor.fetchall()
    return render(request, "popup-create-album.html", {"labels" : labels})


@csrf_exempt
def show_create_song(request):
    query = """
    SELECT id, judul
    FROM ALBUM"""
    with connection.cursor() as cursor:
        cursor.execute(query)
        albums = cursor.fetchall()

    query = """
    SELECT AR.id, AK.nama
    FROM ARTIST AR
    JOIN AKUN AK ON AR.email_akun = AK.email"""
    with connection.cursor() as cursor:
        cursor.execute(query)
        artists = cursor.fetchall()

    query = """
    SELECT SW.id, AK.nama
    FROM SONGWRITER SW
    JOIN AKUN AK ON SW.email_akun = AK.email"""
    with connection.cursor() as cursor:
        cursor.execute(query)
        songwriters = cursor.fetchall()

    query = """
    SELECT DISTINCT genre
    FROM GENRE"""
    with connection.cursor() as cursor:
        cursor.execute(query)
        genres = cursor.fetchall()
        genres_list = [genre[0] for genre in genres]

    return render(request, "popup-create-song.html", {"albums" :albums, "artists":artists, "songwriters":songwriters, "genres_list":genres_list})

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


@csrf_exempt
def delete_album(request, type):
    judul_album = type
    if request.method == 'POST':
        try:
            # Delete the podcast and cascade delete episodes
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM ALBUM WHERE judul = %s", [judul_album])
                connection.commit()
            
            return redirect('marmut_album:show_kelola_album_label',)

        except Exception as e:
            connection.rollback()
            return HttpResponse('Terjadi kesalahan saat menghapus data dari database: {}'.format(str(e)))
    else:
        return HttpResponseNotAllowed(['POST'])


@csrf_exempt
def delete_song(request, type):
    id_lagu = type
    if request.method == 'POST':
        try:
            # Delete the podcast and cascade delete episodes
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM SONGWRITER_WRITE_SONG WHERE id_song = %s", [id_lagu])
                cursor.execute("DELETE FROM GENRE WHERE id_konten = %s", [id_lagu])
                cursor.execute("DELETE FROM SONG WHERE id_konten = %s", [id_lagu])
                cursor.execute("DELETE FROM KONTEN WHERE id = %s", [id_lagu])
                connection.commit()
            
            return redirect('marmut_album:show_kelola_album_artis_sw',)

        except Exception as e:
            connection.rollback()
            return HttpResponse('Terjadi kesalahan saat menghapus data dari database: {}'.format(str(e)))
    else:
        return HttpResponseNotAllowed(['POST'])
    

@csrf_exempt
def insert_album(request):
    if request.method == 'POST':
        # Mendapatkan nilai judul dari formulir
        judul = request.POST.get('judul')
        label = request.POST.get('label')

        try:
            # Menjalankan kueri untuk menambahkan data ke dalam tabel ALBUM
            with connection.cursor() as cursor:
                new_id = uuid.uuid4()
                cursor.execute("INSERT INTO ALBUM (id, judul, jumlah_lagu, id_label, total_durasi) VALUES (%s, %s, %s, %s, %s)", [new_id, judul, 0, label, 0])

            # Commit perubahan ke dalam database
            connection.commit()

            # Memberikan respons berhasil
            return redirect('marmut_album:show_kelola_album_artis_sw')

        except Exception as e:
            # Rollback jika terjadi kesalahan
            connection.rollback()
            return HttpResponse('Terjadi kesalahan saat menambahkan data ke dalam database: {}'.format(str(e)))

    else:
        return HttpResponse('Metode permintaan tidak diizinkan.')


@csrf_exempt
def insert_song(request):
    if request.method == 'POST':
        # Mendapatkan nilai judul dari formulir
        judul = request.POST.get('judul')
        durasi = request.POST.get('durasi')
        artist = request.POST.get('artist')
        album = request.POST.get('album')
        genres = request.POST.getlist('genre[]')
        songwriters = request.POST.getlist('songwriter[]')
        new_id = uuid.uuid4()
        tanggal_rilis = date.today()
        tahun_rilis = tanggal_rilis.year

        try:
            # Menjalankan kueri untuk menambahkan data ke dalam tabel KONTEN
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO KONTEN (id, judul, tanggal_rilis, tahun, durasi) VALUES (%s, %s, %s, %s, %s)", [new_id, judul, tanggal_rilis, tahun_rilis, durasi])
            # Menjalankan kueri untuk menambahkan data ke dalam tabel GENRE
            for genre in genres:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO GENRE (id_konten, genre) VALUES (%s, %s)", [new_id, genre])
            # Menjalankan kueri untuk menambahkan data ke dalam tabel SONG
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO SONG (id_konten, id_artist, id_album, total_play, total_download) VALUES (%s, %s, %s, %s, %s)", [new_id, artist, album, 0, 0])
            # Menjalankan kueri untuk menambahkan data ke dalam tabel SONGWRITER_WRITE_SONG
            for songwriter in songwriters:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO SONGWRITER_WRITE_SONG (id_songwriter, id_song) VALUES (%s, %s)", [songwriter, new_id])

            # Commit perubahan ke dalam database
            connection.commit()

            # Memberikan respons berhasil
            return redirect('marmut_album:show_kelola_album_artis_sw')

        except Exception as e:
            # Rollback jika terjadi kesalahan
            connection.rollback()
            return HttpResponse('Terjadi kesalahan saat menambahkan data ke dalam database: {}'.format(str(e)))

    else:
        return HttpResponse('Metode permintaan tidak diizinkan.')