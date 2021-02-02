from rest_framework import serializers
from .models import Movie, PersonPosition, Genre, Person
from .logic.data_structures.enums import Positions
from api.management.commands.etl import movie_to_dict


class GenreSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        return instance.name

    def to_internal_value(self, data):
        ret = {
            "name" : data
        }
        return ret

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

    def to_internal_value(self, data):
        ret = {
            "person_id" : {
                "name" : data.get('person_id')
            },
            "position" : data.get('position')
        }
        return ret

    class Meta:
        model = PersonPosition
        fields = ('person_id', 'position')


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

    def create(self, validated_data):
        genres_name = []
        genres = validated_data.pop('genre')
        for genre in genres:
            name = genre.values()
            genres_name.append(*name)
        
        crew = validated_data.pop('personposition_set')

        instance = Movie.objects.create(**validated_data)
        person_positions = [
                PersonPosition.objects.create(
                    movie_id=instance,
                    person_id=Person.objects.get(name=person.get('person_id').get('name')),
                    position=person.get('position')
                ) for person in crew
            ]
        genre = Genre.objects.filter(name__in=genres_name)
        instance.genre.set(genre)
        instance.personposition_set.set(person_positions)
        return instance
    
    def update(self, instance, validated_data):
        genres = validated_data.pop('genre')
        crew = validated_data.pop('personposition_set')

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        
        genres = Genre.objects.filter(name__in=[genre.get('name') for genre in genres])
        instance.genre.set(genres)

        [person_position.delete() for person_position in instance.personposition_set.all()]
        person_positions = [
                PersonPosition.objects.create(
                    movie_id=instance,
                    person_id=Person.objects.get(name=person.get('person_id').get('name')),
                    position=person.get('position')
                ) for person in crew
            ]
        instance.personposition_set.set(person_positions)
        return instance