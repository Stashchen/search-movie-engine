from rest_framework.serializers import ModelSerializer

from .models import Movies


class MoviesSerializer(ModelSerializer):

    class Meta:
        model = Movies
        fields = (
            'id', 
            'title', 
            'description', 
            'genre', 
            'director', 
            'imdb_rating'
        )