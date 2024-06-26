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

        account = False
        label = False

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM akun WHERE email = %s AND password = %s", [email, password])
                data = cursor.fetchall()

                if data:
                    account = True
                else:
                    cursor.execute("SELECT * FROM label WHERE email = %s AND password = %s", [email, password])
                    data = cursor.fetchall()
                    if data:
                        label = True

        except Exception as e:
            print(e)
            context = {"is_error": True}
            return render(request, 'test.html', context)

        if account:
            email = data[0][0]
            nama = data[0][2]
            gender = data[0][3]
            tempat_lahir = data[0][4]
            tanggal_lahir = data[0][5]
            is_verified = data[0][6]
            kota_asal = data[0][7]
            podcaster = False
            artist = False
            songwriter = False

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM podcaster WHERE email = %s", [email])
                if cursor.fetchall():
                    podcaster = True
                cursor.execute("SELECT * FROM artist WHERE email_akun = %s", [email])
                if cursor.fetchall():
                    artist = True
                cursor.execute("SELECT * FROM songwriter WHERE email_akun = %s", [email])
                if cursor.fetchall():
                    songwriter = True

            response = HttpResponseRedirect(reverse('marmut_app:show_dashboard'))

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
            roles = []
            if podcaster:
                roles.append('podcaster')
            if artist:
                roles.append('artist')
            if songwriter:
                roles.append('songwriter')
            if not podcaster and not artist and not songwriter:
                roles.append('biasa')
            sleep(1)
            response.set_cookie('role', ', '.join(roles))
            print(request.COOKIES.get('role'))
            return response

        elif label:
            id = data[0][0]
            nama = data[0][1]
            email = data[0][2]
            kontak = data[0][4]
            id_pemilik_hak_cipta = data[0][5]

            response = HttpResponseRedirect(reverse('marmut_app:show_dashboard'))

            # Set cookies based on roles
            response.set_cookie('id', id)
            response.set_cookie('nama', nama)
            response.set_cookie('is_authenticated', True)
            response.set_cookie('kontak', kontak)
            response.set_cookie('id_pemilik_hak_cipta', id_pemilik_hak_cipta)
            response.set_cookie('role', 'label')
            return response

        else:
            context = {"is_error": True}

    return render(request, 'auth_login.html', context)



def logout(request):
    # Create a redirect response to the main page
    response = render(request, "main.html")
    print(request.COOKIES.get('nama'))

    # Delete all the cookies
    if (request.COOKIES.get('role') == 'label'):
        response.delete_cookie('id', id)
        response.delete_cookie('nama')
        response.delete_cookie('is_authenticated')
        response.delete_cookie('kontak')
        response.delete_cookie('id_pemilik_hak_cipta')
        response.delete_cookie('label')
    else:
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