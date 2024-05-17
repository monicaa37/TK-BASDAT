import uuid
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.db import connection
from datetime import datetime, timedelta, date
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def insert_data(request):
    if request.method == 'POST':
        # Mendapatkan nilai judul dari formulir
        judul = request.POST.get('judulPodcast')

        # Mendapatkan nilai genre dari formulir
        genres = request.POST.getlist('genre')
        # Mendapatkan email podcaster dari cookie
        email_podcaster = request.COOKIES.get('email')
        print(f"Judul: {judul}")
        print(f"Genre: {', '.join(genres)}")
        print(f"email: {email_podcaster}")

        # Mendapatkan tanggal saat ini dan tahun saat ini
        tanggal_rilis = datetime.now()
        tahun = tanggal_rilis.year

        try:
            # Menjalankan kueri untuk menambahkan data ke dalam tabel KONTEN
            with connection.cursor() as cursor:
                new_id = uuid.uuid4()
                cursor.execute("INSERT INTO KONTEN (id, judul, tanggal_rilis, tahun, durasi) VALUES (%s, %s, %s, %s, %s)", [new_id, judul, tanggal_rilis, tahun, 0])

            # Menjalankan kueri untuk menambahkan data ke dalam tabel PODCAST
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO PODCAST (id_konten, email_podcaster) VALUES (%s, %s)", [new_id, email_podcaster])

            # Menjalankan kueri untuk menambahkan data ke dalam tabel GENRE sebanyak genre yang dipilih
            with connection.cursor() as cursor:
                for genre in genres:
                    cursor.execute("INSERT INTO GENRE (id_konten, genre) VALUES (%s, %s)", [new_id, genre])

            # Commit perubahan ke dalam database
            connection.commit()

            # Memberikan respons berhasil
            return redirect('marmut_podcast:show_list_podcast')

        except Exception as e:
            # Rollback jika terjadi kesalahan
            connection.rollback()
            return HttpResponse('Terjadi kesalahan saat menambahkan data ke dalam database: {}'.format(str(e)))

    else:
        return HttpResponse('Metode permintaan tidak diizinkan.')

@csrf_exempt
def delete_podcast(request, type):
    podcast_id = type
    if request.method == 'POST':
        try:
            # Delete the podcast and cascade delete episodes
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM PODCAST WHERE id_konten = %s", [podcast_id])
                connection.commit()
            
            return redirect('marmut_podcast:show_list_podcast')

        except Exception as e:
            connection.rollback()
            return HttpResponse('Terjadi kesalahan saat menghapus data dari database: {}'.format(str(e)))
    else:
        return HttpResponseNotAllowed(['POST'])

def show_list_podcast(request):
    try:
        podcasts = []
        query = """
        SELECT
            P.id_konten AS id,
            K.judul AS Judul,
            COUNT(E.id_episode) AS "Jumlah Episode",
            SUM(E.durasi) AS "Total Durasi"
        FROM
            PODCAST P
        JOIN
            KONTEN K ON P.id_konten = K.id
        LEFT JOIN
            EPISODE E ON P.id_konten = E.id_konten_podcast
        GROUP BY
            P.id_konten, K.judul;
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            podcasts = cursor.fetchall()
    except Exception as e:
        print("Error:", e)
        podcasts = []
    return render(request, 'list-podcast.html', {"podcasts" : podcasts})


def play_podcast(request, type):
    id_konten = type
    podcast_detail = {}
    genres_list = []

    with connection.cursor() as cursor:
        # Query to fetch podcast details
        cursor.execute("""
            SELECT 
                K.judul AS podcast_title,
                STRING_AGG(G.genre, ', ') AS genres,
                A.nama AS podcaster_name,
                SUM(E.durasi) AS total_duration,
                K.tanggal_rilis AS release_date,
                EXTRACT(YEAR FROM K.tanggal_rilis) AS release_year
            FROM 
                KONTEN K
            JOIN 
                PODCAST P ON K.id = P.id_konten
            JOIN 
                PODCASTER PD ON P.email_podcaster = PD.email
            JOIN 
                EPISODE E ON P.id_konten = E.id_konten_podcast
            JOIN 
                GENRE G ON K.id = G.id_konten
            JOIN 
                AKUN A ON PD.email = A.email
            WHERE 
                K.id = %s
            GROUP BY 
                K.judul, A.nama, K.tanggal_rilis
        """, [id_konten])
        
        row = cursor.fetchone()
        if row:
            podcast_detail = {
                'podcast_title': row[0],
                'genres': row[1].split(', '),  # Split genres into a list
                'podcaster_name': row[2],
                'total_duration': row[3],
                'release_date': row[4].strftime('%Y-%m-%d'),  # Format date as string
                'release_year': row[5]
            }
            genres_list = podcast_detail['genres']
    
    # Eksekusi query SQL
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT KONTEN.judul AS Judul,
                   EPISODE.id_episode AS Id_Episode,
                   EPISODE.judul AS Judul_Episode,
                   EPISODE.deskripsi AS Deskripsi,
                   EPISODE.durasi AS Durasi,
                   EPISODE.tanggal_rilis AS Tanggal
            FROM PODCAST
            JOIN KONTEN ON PODCAST.id_konten = KONTEN.id
            JOIN EPISODE ON PODCAST.id_konten = EPISODE.id_konten_podcast
            WHERE PODCAST.id_konten = %s
        """, [id_konten])

        # Ambil semua baris hasil query
        episodes = cursor.fetchall()

    # Ubah hasil query menjadi list of dictionaries untuk kemudahan akses di template
    episodes = [{'Judul': episode[0], 'Id_Episode': episode[1], 'Judul_Episode': episode[2], 'Deskripsi': episode[3], 'Durasi': episode[4], 'Tanggal': episode[5]} for episode in episodes]

    return render(request, 'play-podcast.html', {
        'podcast_detail': podcast_detail,
        'genres_list': genres_list, 'episodes':episodes
    })


def show_top_charts(request):
    context = {
        '':''
    }

    return render(request, "top-charts.html", context)

def show_create_podcast(request):
    context = {
        '':''
    }

    return render(request, "create-podcast.html", context)


def show_list_episode_podcast(request, type):
    # Dapatkan id_konten dari URL
    id_konten = type

    # Eksekusi query SQL
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT KONTEN.judul AS Judul,
                   EPISODE.id_episode AS Id_Episode,
                   EPISODE.judul AS Judul_Episode,
                   EPISODE.deskripsi AS Deskripsi,
                   EPISODE.durasi AS Durasi,
                   EPISODE.tanggal_rilis AS Tanggal
            FROM PODCAST
            JOIN KONTEN ON PODCAST.id_konten = KONTEN.id
            JOIN EPISODE ON PODCAST.id_konten = EPISODE.id_konten_podcast
            WHERE PODCAST.id_konten = %s
        """, [id_konten])

        # Ambil semua baris hasil query
        episodes = cursor.fetchall()

    # Ubah hasil query menjadi list of dictionaries untuk kemudahan akses di template
    episodes = [{'Judul': episode[0], 'Id_Episode': episode[1], 'Judul_Episode': episode[2], 'Deskripsi': episode[3], 'Durasi': episode[4], 'Tanggal': episode[5]} for episode in episodes]

    # Ambil detail podcast
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT KONTEN.judul AS Judul
            FROM KONTEN
            WHERE KONTEN.id = %s
        """, [id_konten])

        # Ambil detail podcast
        podcast_detail = cursor.fetchone()

    # Render template dengan data yang sudah diambil
    return render(request, 'list-episode-podcast.html', {'episodes': episodes, 'podcast_detail': podcast_detail})

def create_episode(request, type):
    if request.method == 'POST':
        id_konten = type
        # Generate UUID for id_episode
        id_episode = uuid.uuid4()
        judul = request.POST.get('judulInput')
        deskripsi = request.POST.get('deskripsiInput')
        durasi = request.POST.get('durasiInput')
        tanggal_rilis = date.today()

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO EPISODE (id_episode, id_konten_podcast, judul, deskripsi, durasi, tanggal_rilis)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, [id_episode,id_konten, judul, deskripsi, durasi, tanggal_rilis])

        return redirect('marmut_podcast:show_list_episode_podcast', type=id_konten)
    else:
        # Jika bukan request POST, tampilkan form kosong
        id_konten = type
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT KONTEN.judul AS Judul
                FROM KONTEN
                WHERE KONTEN.id = %s
            """, [id_konten])
            podcast_detail = cursor.fetchone()
            podcast_id = id_konten

        return render(request, "create-episode.html", {'podcast_detail': podcast_detail, 'podcast_id':podcast_id})

@csrf_exempt
def delete_episode(request, type):
    episode_id = type
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM EPISODE
                WHERE id_episode = %s
            """, [episode_id])
        
        # Optionally, you can redirect to the list of episodes or a success page
        return redirect('marmut_podcast:show_list_podcast')
    else:
        return HttpResponseNotAllowed(['POST'])

def chart_detail(request, type):
    try:
        current_date = datetime.now().date()
        chart_title = ""
        params = []

        if type == 'daily':
            query = """
                SELECT 
                    K.judul AS "Judul Lagu",
                    AK.nama AS "Oleh",
                    K.tanggal_rilis AS "Tanggal Rilis",
                    S.total_play AS "Total Plays"
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
                WHERE 
                    APS.waktu::date = %s
                ORDER BY 
                    S.total_play DESC
                LIMIT 20;
            """
            params = [current_date]
            chart_title = "Daily Top 20"
        elif type == 'weekly':
            weekly_start_date = current_date - timedelta(days=current_date.weekday())
            query = """
                SELECT 
                    K.judul AS "Judul Lagu",
                    AK.nama AS "Oleh",
                    K.tanggal_rilis AS "Tanggal Rilis",
                    S.total_play AS "Total Plays"
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
                WHERE 
                    APS.waktu::date >= %s AND APS.waktu::date <= %s
                ORDER BY 
                    S.total_play DESC
                LIMIT 20;
            """
            params = [weekly_start_date, current_date]
            chart_title = "Weekly Top 20"
        elif type == 'monthly':
            monthly_start_date = current_date.replace(day=1)
            query = """
                SELECT 
                    K.judul AS "Judul Lagu",
                    AK.nama AS "Oleh",
                    K.tanggal_rilis AS "Tanggal Rilis",
                    S.total_play AS "Total Plays"
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
                WHERE 
                    APS.waktu::date >= %s AND APS.waktu::date <= %s
                ORDER BY 
                    S.total_play DESC
                LIMIT 20;
            """
            params = [monthly_start_date, current_date]
            chart_title = "Monthly Top 20"
        elif type == 'yearly':
            yearly_start_date = current_date.replace(month=1, day=1)
            query = """
                SELECT 
                    K.judul AS "Judul Lagu",
                    AK.nama AS "Oleh",
                    K.tanggal_rilis AS "Tanggal Rilis",
                    S.total_play AS "Total Plays"
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
                WHERE 
                    APS.waktu::date >= %s AND APS.waktu::date <= %s
                ORDER BY 
                    S.total_play DESC
                LIMIT 20;
            """
            params = [yearly_start_date, current_date]
            chart_title = "Yearly Top 20"

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            chart_data = cursor.fetchall()

    except Exception as e:
        print("Error:", e)
        chart_data = []

    return render(request, "chart-detail.html", {"chart_data": chart_data, "chart_title": chart_title})
