import requests
import json

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.migrations.executor import MigrationExecutor
from django.db import connections, DEFAULT_DB_ALIAS
from django.forms.models import model_to_dict

from progress.bar import Bar
from requests.models import Request

from api.models import Movie, Person, PersonPosition
from api.logic.data_structures.enums import Positions

from uuid import uuid4

from ._sqlite_models import (
    Actors,
    MovieActors,
    Movies,
    Writers,
    People
)


def etl_person():
    Person.objects.bulk_create([
        Person(name=people_name) for people_name in People.all_person()
    ])

def etl_movie():
    genres = set()
    for index, movie in enumerate(Movies.select().execute(), start=1):
        print(index)
        movie_dict = movie.to_dict()
        
        genres = genres.union({genre for genre in movie_dict.pop('genre')})
        directors = Person.objects.filter(name__in=movie_dict.pop('director'))
        actors = Person.objects.filter(name__in=movie.get_actors())
        writers = Person.objects.filter(name__in=movie.get_writers())
        
        movie_django = Movie.objects.create(
            id=uuid4(),
            title=movie_dict.get('title'),
            description=movie_dict.get('plot'),
            imdb_rating=movie_dict.get('imdb_rating')
        )
        for position, peoples in zip(Positions, [writers, actors, directors]):
            # print(position)
            PersonPosition.objects.bulk_create([
                PersonPosition(
                    movie_id=movie_django,
                    person_id=people,
                    position=position
                ) for people in peoples
            ])


        
        


class Command(BaseCommand):
    help = 'Load data from SQLite database to PostgreSQL and to elasticsearch'

    def handle(self, *args, **options):
        pass
        # print(len([writer_name for writer_name in Actors.get_names()]))
        # init_es()
        # if is_database_synchronized(DEFAULT_DB_ALIAS):
        #     print('All migrations have been applied.')
        #     load_movies_es(extract_movies())
        #     print("All data is transfered to elasticsearch")
        # else:
        #     print("Unapplied migrations found.")