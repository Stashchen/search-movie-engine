from rest_framework.serializers import ModelSerializer
from rest_framework.fields import JSONField

# from django.forms.fields import 
from .models import Movies, Writers, Actors


class WriterSerializer(ModelSerializer):
    class Meta:
        model = Writers
        fields = (
            'id',
            'name'
        )

class ActorSerializer(ModelSerializer):
    class Meta:
        model = Actors
        fields = (
            'id',
            'name'
        )

class MoviesSerializer(ModelSerializer):
    writers = WriterSerializer()
    class Meta:
        model = Movies
        fields = (
            'id', 
            'title', 
            'description', 
            'genre', 
            'director', 
            'imdb_rating',
            'writers',
            'actors'
        )