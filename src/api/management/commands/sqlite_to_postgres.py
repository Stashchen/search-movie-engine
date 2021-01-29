from uuid import uuid4
from progress.bar import Bar

from django.core.management.base import BaseCommand
from django.core.management import call_command
from api.models import Movie, Person, PersonPosition, Genre
from api.logic.data_structures.enums import Positions
from api.management.commands._sqlite_models import (
    Movies,
    People
)

def etl_person():
    Person.objects.bulk_create([
        Person(name=people_name) for people_name in People.all_person()
    ])



def etl_movie():
    # Load all person (actors, directors and writers)
    # etl_person()

    # Load all other data (movies, genres and person_position)
    bar = Bar("processing", max=Movies.select().count())
    bar.start()
    for movie in Movies.select().execute():
        movie_dict = movie.to_dict() # Convert movie to dict and modificate some data
        
        genres = [Genre.objects.get_or_create(name=genre)[0] for genre in movie_dict.get('genre')] 
        directors = Person.objects.filter(name__in=movie_dict.get('director'))
        actors = Person.objects.filter(name__in=movie.get_actors())
        writers = Person.objects.filter(name__in=movie.get_writers())
        
        movie_django = Movie.objects.create(
            id=uuid4(),
            title=movie_dict.get('title'),
            description=movie_dict.get('plot'),
            imdb_rating=movie_dict.get('imdb_rating')
        )
        movie_django.genre.set(genres)

        # Add data to PersonPosition model for one movie
        for position, peoples in zip(Positions, [writers, actors, directors]):
            PersonPosition.objects.bulk_create([
                PersonPosition(
                    movie_id=movie_django,
                    person_id=people,
                    position=position
                ) for people in peoples
            ])
        bar.next()
    bar.finish()


class Command(BaseCommand):
    help = 'Load data from SQLite database to PostgreSQL and to elasticsearch'

    def handle(self, *args, **options):
        call_command("flush", '--noinput')
        etl_person()
        etl_movie()
        print("All data are transfered from sqlite to postgresql")