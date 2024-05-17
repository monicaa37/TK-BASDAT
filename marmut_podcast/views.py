from django.shortcuts import render
from django.db import connection
from datetime import datetime, timedelta

def send_id_konten(request):
    id_konten = '8738b6a1-51ae-4c33-812d-ec8919e60f8d'
    return show_play_podcast(request, id_konten)

def show_play_podcast(request, id_konten):
    genres_list = []  # Initialize genres_list outside of the try block
    try:
        with connection.cursor() as cursor:
            # Mendapatkan detail podcast
            cursor.execute("""
                SELECT 
                    p.id_konten AS id_podcast,
                    k.judul AS podcast_title,
                    GROUP_CONCAT(g.genre SEPARATOR ', ') AS genres,
                    a.nama AS podcaster_name,
                    SEC_TO_TIME(SUM(e.durasi * 60)) AS total_duration,
                    DATE_FORMAT(k.tanggal_rilis, '%d/%m/%y') AS release_date,
                    k.tahun AS release_year
                FROM 
                    PODCAST p
                JOIN 
                    KONTEN k ON p.id_konten = k.id
                JOIN 
                    GENRE g ON k.id = g.id_konten
                JOIN 
                    PODCASTER po ON p.email_podcaster = po.email
                JOIN 
                    AKUN a ON po.email = a.email
                JOIN 
                    EPISODE e ON e.id_konten_podcast = p.id_konten
                WHERE 
                    p.id_konten = %s
                GROUP BY 
                    p.id_konten, k.judul, a.nama, k.tanggal_rilis, k.tahun;
            """, [id_konten])
            podcast_detail = cursor.fetchone()

            if podcast_detail:
                # Split the genres string into a list
                genres_list = podcast_detail['genres'].split(', ')

                # Mendapatkan daftar episode untuk podcast tertentu
                cursor.execute("""
                    SELECT 
                        e.judul AS episode_title,
                        e.deskripsi AS episode_description,
                        SEC_TO_TIME(e.durasi * 60) AS episode_duration,
                        DATE_FORMAT(e.tanggal_rilis, '%d/%m/%Y') AS episode_release_date
                    FROM 
                        EPISODE e
                    JOIN 
                        PODCAST p ON e.id_konten_podcast = p.id_konten
                    JOIN 
                        KONTEN k ON p.id_konten = k.id
                    WHERE 
                        p.id_konten = %s
                    ORDER BY 
                        e.tanggal_rilis;
                """, [id_konten])
                episodes = cursor.fetchall()
            else:
                episodes = []

    except Exception as e:
        print("Error:", e)
        podcast_detail = None
        episodes = []

    context = {
        "podcast_detail": podcast_detail,
        "genres_list": genres_list,  # Add genres_list to the context
        "episodes": episodes
    }

    return render(request, "play-podcast.html", context)

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
