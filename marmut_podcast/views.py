from django.shortcuts import render
from django.db import connection
from datetime import datetime, timedelta

def show_list_podcast(request):
    try:
        podcasts = []
        query = """
        SELECT 
            KONTEN.judul AS Judul,
            COUNT(EPISODE.id_episode) AS "Jumlah Episode",
            SUM(EPISODE.durasi) AS "Total Durasi"
        FROM 
            PODCAST
        JOIN 
            KONTEN ON PODCAST.id_konten = KONTEN.id
        LEFT JOIN 
            EPISODE ON PODCAST.id_konten = EPISODE.id_konten_podcast
        GROUP BY 
            KONTEN.judul
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

def show_list_podcast(request):
    context = {
        '':''
    }

    return render(request, "list-podcast.html", context)
def show_list_episode_podcast(request):
    context = {
        '':''
    }

    return render(request, "list-episode-podcast.html", context)
def show_create_podcast(request):
    context = {
        '':''
    }

    return render(request, "create-podcast.html", context)
def show_create_episode(request):
    context = {
        '':''
    }

    return render(request, "create-episode.html", context)


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
