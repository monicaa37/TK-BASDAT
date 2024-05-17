from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection, transaction
from datetime import datetime
import uuid

def insert_label(request):
    if request.method == 'POST':
        id = uuid.uuid4()
        email = request.POST.get('email')
        password = request.POST.get('password')
        nama = request.POST.get('nama')
        kontak = request.POST.get('kontak')

        with connection.cursor() as cursor:
            try:
                cursor.execute("INSERT INTO LABEL (id, nama, email, password, kontak, id_pemilik_hak_cipta) VALUES (%s, %s, %s, %s, %s, NULL)", [id, nama, email, password, kontak])
            except Exception as e:
                return HttpResponse("Error: {}".format(str(e)))

        return HttpResponse("Label successfully registered.")
    else:
        return HttpResponse("Invalid request method.")
    
def register(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        gender = int(request.POST.get('gender'))
        place_of_birth = request.POST.get('place_of_birth')
        date_of_birth = request.POST.get('date_of_birth')
        city = request.POST.get('city')
        roles = request.POST.getlist('roles[]')

        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO AKUN (email, password, nama, gender, tempat_lahir, tanggal_lahir, is_verified, kota_asal) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, [email, password, name, gender, place_of_birth, date_of_birth, False, city])

                    for role in roles:
                        if role == "podcaster":
                            cursor.execute("""
                                INSERT INTO PODCASTER (email)
                                VALUES (%s)
                            """, [email])
                        elif role == "artist":
                            artist_id = uuid.uuid4()
                            cursor.execute("""
                                INSERT INTO ARTIST (id, email_akun, id_pemilik_hak_cipta)
                                VALUES (%s, %s, NULL)
                            """, [artist_id, email])
                        elif role == "songwriter":
                            songwriter_id = uuid.uuid4()
                            cursor.execute("""
                                INSERT INTO SONGWRITER (id, email_akun, id_pemilik_hak_cipta)
                                VALUES (%s, %s, NULL)
                            """, [songwriter_id, email])

            return redirect('marmut_podcast:show_list_podcast')
        except Exception as e:
            print("Error:", e)
            # Handle error, for example, show an error message
            return render(request, 'user-regist.html', {'error_message': 'Registration failed, please try again.'})

    return HttpResponse("User successfully registered.")


# Create your views here.
def show_main(request):
    context = {
        '': '',
    }

    return render(request, "main.html", context)

def show_main_asli(request):
    return render(request, "main.html")

def show_registerpage(request):
    context = {
        '': '',
    }

    return render(request, "registration-page.html", context)

def show_login(request):
    context = {
        '': '',
    }

    return render(request, "login.html", context)

def show_user_regist(request):
    context = {
        '': '',
    }

    return render(request, "user-regist.html", context)

def show_label_regist(request):
    context = {
        '': '',
    }

    return render(request, "label-regist.html", context)


def show_artist_song(request):
    context = {
        '': '',
    }

    return render(request, "dashboard-artist-songwriter.html", context)

def show_dashboard(request):
    roles = request.COOKIES.get('role')
    print(roles)
    
    if 'label' in roles:
        query = """
            SELECT A.judul AS "Judul Album",
                   A.jumlah_lagu AS "Jumlah Lagu di Album"
            FROM ALBUM A
            JOIN LABEL L ON A.id_label = L.id
            WHERE L.id = %s"""
        with connection.cursor() as cursor:
            cursor.execute(query, [request.COOKIES.get('id')])
            albums = cursor.fetchall()
        return render(request, "dashboard.html", {"albums": albums})


    else:
        podcasts = None
        songs = None
        playlists = None

        if 'podcaster' in roles:
            query = """
                SELECT K.judul AS podcast_title
                FROM KONTEN K
                JOIN PODCAST P ON K.id = P.id_konten
                JOIN PODCASTER PR ON P.email_podcaster = PR.email
                WHERE PR.email = %s"""
            with connection.cursor() as cursor:
                cursor.execute(query, [request.COOKIES.get('email')])
                podcasts = cursor.fetchall()


        if 'artist' in roles or 'songwriter' in roles:
            songs = []
            if 'artist' in roles:
                query_artist = """
                    SELECT K.judul AS song_title
                    FROM KONTEN K
                    JOIN SONG S ON K.id = S.id_konten
                    JOIN ARTIST A ON S.id_artist = A.id
                    WHERE A.email_akun = %s"""
                with connection.cursor() as cursor:
                    cursor.execute(query_artist, [request.COOKIES.get('email')])
                    artist_songs = cursor.fetchall()
                songs.extend(artist_songs)

            if 'songwriter' in roles:
                print(request.COOKIES.get('email'))
                query_sw = """
                    SELECT K.judul AS song_title
                    FROM KONTEN K
                    JOIN SONGWRITER_WRITE_SONG SWS ON K.id = SWS.id_song
                    JOIN SONGWRITER SW ON SWS.id_songwriter = SW.id
                    WHERE SW.email_akun = %s"""
                with connection.cursor() as cursor:
                    cursor.execute(query_sw, [request.COOKIES.get('email')])
                    sw_songs = cursor.fetchall()
                songs.extend(sw_songs)


        if 'biasa' in roles or 'premium' in roles:
            query = """
                SELECT judul AS playlist_title
                FROM USER_PLAYLIST
                WHERE email_pembuat = %s"""
            with connection.cursor() as cursor:
                cursor.execute(query, [request.COOKIES.get('email')])
                playlists = cursor.fetchall()

        return render(request, "dashboard.html", {"podcasts": podcasts, "songs": songs, "playlists": playlists})