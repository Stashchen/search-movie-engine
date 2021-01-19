from django.urls import path

from .views import MovieList


app_name = 'api'

urlpatterns = [
    path('movies/', MovieList.as_view(), name='movies')
]