from time import sleep
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.db import connection

def test(request):
    return render(request, "test.html")

@csrf_exempt
def login(request):
    context = {"error": ""}
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM akun WHERE email = '{email}' AND password = '{password}'")
                data = cursor.fetchall()
        except Exception as e:
            print(e)
            context = {"is_error": True}
            return render(request, 'test.html', context)

        if len(data) != 0:
            email = data[0][0]
            nama = data[0][2]
            gender = data[0][3]
            tempat_lahir = data[0][4]
            tanggal_lahir = data[0][5]
            is_verified = data[0][6]
            kota_asal = data[0][6]
            podcaster = False
            artist = False
            songwriter = False

            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM podcaster WHERE email = '{email}'")
                if cursor.fetchall():
                    podcaster = True
                cursor.execute(f"SELECT * FROM artist WHERE email_akun = '{email}'")
                if cursor.fetchall():
                    artist = True
                cursor.execute(f"SELECT * FROM songwriter WHERE email_akun = '{email}'")
                if cursor.fetchall():
                    songwriter = True

            response = HttpResponseRedirect(reverse('auth:test'))

            # Set cookies based on roles
            response.set_cookie('email', email)
            response.set_cookie('nama', nama)
            response.set_cookie('is_authenticated', True)
            response.set_cookie('gender', gender)
            response.set_cookie('tempat_lahir', tempat_lahir)
            response.set_cookie('tanggal_lahir', tanggal_lahir)
            response.set_cookie('is_verified', is_verified)
            response.set_cookie('kota_asal', kota_asal)

            # Set role cookies
            if podcaster:
                response.set_cookie('podcaster', True)
            if artist:
                response.set_cookie('artist', True)
            if songwriter:
                response.set_cookie('songwriter', True)
            if not (podcaster or artist or songwriter):
                response.set_cookie('biasa', True)
            sleep(1)
            return response
        else:
            context = {"is_error": True}

    return render(request, 'auth_login.html', context)

def logout(request):
    # Create a redirect response to the main page
    response = render(request, "auth_login.html")
    print(request.COOKIES.get('nama'))

    # Delete all the cookies
    response.delete_cookie('email')
    response.delete_cookie('nama')
    response.delete_cookie('is_authenticated')
    response.delete_cookie('gender')
    response.delete_cookie('tempat_lahir')
    response.delete_cookie('tanggal_lahir')
    response.delete_cookie('is_verified')
    response.delete_cookie('kota_asal')
    response.delete_cookie('podcaster')
    response.delete_cookie('artist')
    response.delete_cookie('songwriter')
    response.delete_cookie('biasa')

    return response


