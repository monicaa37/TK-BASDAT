from django.shortcuts import render

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

def show_label_regist(request):
    context = {
        '': '',
    }

    return render(request, "label-regist.html", context)

def show_label_regist(request):
    context = {
        '': '',
    }

    return render(request, "label-regist.html", context)

def show_label_regist(request):
    context = {
        '': '',
    }

    return render(request, "label-regist.html", context)

def show_label_regist(request):
    context = {
        '': '',
    }
    return render(request, "index.html", context)

def show_dashboard(request):
    return render(request, "dashboard.html")
