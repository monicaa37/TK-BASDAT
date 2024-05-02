from django.urls import path
from marmut_app.views import show_main, show_index

app_name = 'marmut_app'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('index', show_index, name='show_index'),
    
]