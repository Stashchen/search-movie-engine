import requests
import json
from ._peewee_models import (
    Actors as sqlite_actors,
    MovieActors as sqlite_movieactors,
    Movies as sqlite_movies,
    Writers as sqlite_writers
)
import api.models as django_models

from django.core.management.base import BaseCommand



from progress.bar import Bar

BASE_URL = 'http://127.0.0.1:9200'

"""{
    "id": "my pretty text",
    "imdb_rating": 15,
    "genre" : "StarWars",
    "title" : "qwert",
    "description" : "something interesting",
    "director" : "George Lucas",
    "actors_names" : ["qeqweqweqw", "nik"],
    "writers_names" : ["werewrwer"],
    "actors" : [
        {"id": "t0123qwe", "name" : "Nikita Efremov"},
        {"id": "t023", "name" : "Georg"}
    ],
    "writers" : [
        {"id" : "123123", "name" : "Daniil Lapezo"}
    ]
}"""

def extract_movies() -> dict:
    movies = []
    bar = Bar('Processing', max=sqlite_movies.count())
    for movie in sqlite_movies.select().execute():
        data = {}
        data.update(movie.to_dict())
        data["actors_names"] = []
        data["actors"] = []
        for actor in sqlite_movieactors.select(sqlite_movieactors.actor_id).join(sqlite_actors).where(sqlite_movieactors.movie_id == movie.id):
            actor_name = actor.actor_id.name
            if actor_name != "N/A":
                data["actors_names"].append(actor_name)
                data["actors"].append({"id" : actor.actor_id.id, "name" : actor_name})
        data["writers_names"] = []
        data["writers"] = []
        if movie.writers:
            for writer in json.loads(movie.writers):
                name = sqlite_writers.get_name(writer.get("id"))
                if name not in data["writers_names"] and name != "N/A":
                    data["writers_names"].append(name) 
                    data["writers"].append({"id" : writer.get("id"), "name" : name})
        else:
            name = sqlite_writers.get_name(movie.writer)
            if name != "N/A":
                data["writers_names"].append(name)
                data["writers"].append({"id" : movie.writer, "name" : name})
        movies.append(data)
        bar.next()
    bar.finish()
    return movies

def load_movies_es(movies: list):
    url = f"{BASE_URL}/_bulk?filter_path=items.*.error"
    headers = {
        'Content-Type': 'application/x-ndjson'
    }
    payload = ""

    for id, movie in enumerate(movies, start=1):
        payload+=json.dumps(
            {"index": {"_index": "movies", "_id": id}}
        ) + "\n" + json.dumps(movie) + "\n"

    requests.request("POST", url, headers=headers, data=payload)
    
def load_movies_psql():
    bar = Bar('Writers', max=sqlite_writers.select().count())
    for writer in sqlite_writers.select().execute():
        django_models.Writers.objects.create(
            id=writer.id,
            name=writer.name
        )
        bar.next()
    bar.finish()
    bar = Bar('Actors', max=sqlite_actors.select().count())
    for id, actor in enumerate(sqlite_actors.select().execute(), start=1):
        django_models.Actors.objects.create(
            name=actor.name,
            id=id
        )
        bar.next()
    bar.finish()
    bar = Bar('Movies', max=sqlite_movies.select().count())
    movie_writer_id = 1
    for movie in sqlite_movies.select().execute():
        movie_dict = movie.to_dict()
        django_movie = django_models.Movies.objects.create(
            id=movie_dict.get('id'),
            genre=movie_dict.get('genre'),
            director=movie_dict.get('director'),
            title=movie_dict.get('title'),
            plot=movie_dict.get('description'),
            imdb_rating=movie_dict.get('imdb_rating')
        )
        for movie_writer in movie.get_writers():
            django_models.MovieWriters.objects.create(
                id=movie_writer_id,
                movie=django_movie,
                writer=django_models.Writers.objects.get(id=movie_writer)
            )
            movie_writer_id+=1
        bar.next()
    bar.finish()

    bar = Bar('Movie actors', max=sqlite_movieactors.select().count())
    for id, movie_actor in enumerate(sqlite_movieactors.select().execute(), start=1):
        django_models.MovieActors.objects.create(
            id=id,
            movie=django_models.Movies.objects.get(id=movie_actor.movie_id.id),
            actor=django_models.Actors.objects.get(id=movie_actor.actor_id.id)
        )
        bar.next()
    bar.finish()


class Command(BaseCommand):
    help = 'Load data from SQLite database to PostgreSQL and to elasticsearch'

    def handle(self, *args, **options):
        movies = extract_movies()
        load_movies_es(movies)
        load_movies_psql()
        print("All data is transfered to elasticsearch")
