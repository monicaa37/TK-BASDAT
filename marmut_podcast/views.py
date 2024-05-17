import uuid
from django.shortcuts import redirect, render
from django.db import connection
from datetime import datetime, timedelta, date

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


def play_podcast(request):
    # Ambil id konten dari parameter URL atau sesuaikan dengan cara Anda
    id_konten = request.GET.get('id_konten', '')

    # Buat cursor untuk eksekusi query
    with connection.cursor() as cursor:
        # Execute SQL untuk mendapatkan detail podcast
        cursor.execute("""
            SELECT 
                k.judul AS "Judul",
                GROUP_CONCAT(DISTINCT g.genre ORDER BY g.genre SEPARATOR ', ') AS "Genre(s)",
                a.nama AS "Podcaster",
                SUM(e.durasi) AS "Total Durasi",
                k.tanggal_rilis AS "Tanggal Rilis",
                YEAR(k.tanggal_rilis) AS "Tahun"
            FROM 
                PODCAST p
            JOIN 
                KONTEN k ON p.id_konten = k.id
            JOIN 
                GENRE g ON k.id = g.id_konten
            JOIN 
                AKUN a ON p.email_podcaster = a.email
            LEFT JOIN 
                EPISODE e ON p.id_konten = e.id_konten_podcast
            WHERE 
                p.id_konten = %s
            GROUP BY 
                p.id_konten, k.judul, a.nama, k.tanggal_rilis;
        """, [id_konten])
        podcast_detail = cursor.fetchone()

        # Execute SQL untuk mendapatkan daftar episode podcast
        cursor.execute("""
            SELECT 
                e.judul AS "Judul Episode",
                e.deskripsi AS "Deskripsi",
                e.durasi AS "Durasi",
                e.tanggal_rilis AS "Tanggal"
            FROM 
                EPISODE e
            WHERE 
                e.id_konten_podcast = %s
            ORDER BY 
                e.tanggal_rilis;
        """, [id_konten])
        episodes = cursor.fetchall()

    # Render template dengan data yang diperoleh dari database
    return render(request, 'play-podcast.html', {'podcast_detail': podcast_detail, 'episodes': episodes})

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
    episodes = [{'Judul': episode[0], 'Judul_Episode': episode[1], 'Deskripsi': episode[2], 'Durasi': episode[3], 'Tanggal': episode[4]} for episode in episodes]

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
