from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A'
    }

    return render(request, "main.html", context)

def show_index(request):
    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A'
    }
    return render(request, "index.html", context)

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
