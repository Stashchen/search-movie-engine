from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from .models import Movies, Writers, Actors
from pprint import pprint

class WriterSerializer(ModelSerializer):
    class Meta:
        model = Writers
        fields = '__all__'

class ActorSerializer(ModelSerializer):
    class Meta:
        model = Actors
        fields = '__all__'

class MoviesSerializer(ModelSerializer):
    writers = PrimaryKeyRelatedField(many=True, queryset=Writers.objects.all())
    actors = PrimaryKeyRelatedField(many=True, queryset=Actors.objects.all())
    
    class Meta:
        model = Movies
        fields = '__all__'

    