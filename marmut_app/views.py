from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        '': '',
    }

    return render(request, "main.html", context)

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

def show_dashboard_pengguna_biasa(request):
    return render(request, "dashboard-pengguna-biasa.html")

def show_dashboard_pengguna_premium(request):
    return render(request, "dashboard-pengguna-premium.html")

def show_dashboard_artis_sw(request):
    return render(request, "dashboard-artis-sw.html")

def show_dashboard_label(request):
    return render(request, "dashboard-label.html")

def show_dashboard_podcaster(request):
    return render(request, "dashboard-podcaster.html")

def show_dashboard(request):
    return render(request, "dashboard.html")
