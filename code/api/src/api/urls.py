from django.urls import path

from .views import MovieList, MoveDetails


app_name = 'api'

urlpatterns = [
    path('movies/', MovieList.as_view(), name='movies'),
    path('movies/<str:movieID>/', MoveDetails.as_view(), name='move-details')
]