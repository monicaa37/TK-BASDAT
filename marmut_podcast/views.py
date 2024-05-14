from django.shortcuts import render

# Create your views here.
def show_play_podcast(request):
    context = {
        '':''
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
def show_chart_details(request):
    context = {
        '':''
    }

    return render(request, "chart-detail.html", context)