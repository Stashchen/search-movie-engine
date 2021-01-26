from rest_framework import serializers
from .models import Movie, PersonPosition, Genre, Person
from .data_structures import Positions


class GenreSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        return instance.name

    class Meta:
        model = Genre
        fields = '__all__'

class PersonSerializer(serializers.ModelSerializer):
    
    def to_representation(self, instance):
        return instance.name

    class Meta:
        model = Person
        fields = ('name', )

class PersonPositionSerializer(serializers.ModelSerializer):
    
    person_id = PersonSerializer() 

    class Meta:
        model = PersonPosition
        fields = ('id', 'person_id', 'position')


class MovieSerializer(serializers.ModelSerializer):

    genre = GenreSerializer(many=True)
    crew = PersonPositionSerializer(
        source='personposition_set', many=True
    )

    class Meta:
        model = Movie
        fields = (
            'id', 'title', 'description', 'imdb_rating', 'genre', 'crew'
        )
