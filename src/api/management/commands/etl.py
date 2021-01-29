import requests
import json

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations.exceptions import BadMigrationError
from django.db import connections, DEFAULT_DB_ALIAS
from django.forms.models import model_to_dict

from progress.bar import Bar
from requests.models import Request

from api.models import Movie
from api.logic.data_structures.enums import Positions

from pathlib import Path

def init_es() -> Request():
    url = f"{settings.BASE_ES_URL}movies"
    with open(Path(__file__).parent / 'tmp/es_mapping.json', mode='r') as mapping:
        payload=json.load(mapping)
    headers = {
        'Content-Type': 'application/json'
    }

    return requests.request("PUT", url, headers=headers, json=payload)

def movie_to_dict(movie : Movie) -> dict:
    """Convert Movie model to dict for sending data to ElasticSearch
    Args:
        movie (Movie): the movie that you want to convert to ElasticSearch

    Returns:
        dict: Converted Movie model
    """
    data = {}
    data.update(model_to_dict(movie, exclude=["crew", "genre"]))
    data["genre"] = ", ".join([genre.name for genre in movie.genre.all()])
    data["director"] = []
    for director_person in movie.personposition_set.filter(position=Positions.DIRECTOR):
        director_name = director_person.person_id.name
        if director_name != "N/A":
            data["director"].append(director_name)
    data["actors_names"] = []
    data["actors"] = []
    for actor_person in movie.personposition_set.filter(position=Positions.ACTOR):
        actor_name = actor_person.person_id.name
        if actor_name != "N/A":
            data["actors_names"].append(actor_name)
            data["actors"].append({"id" : actor_person.person_id.id, "name" : actor_name})
    data["writers_names"] = []
    data["writers"] = []

    writers = movie.personposition_set.filter(position=Positions.WRITER)
    for writer in writers:
        name = writer.person_id.name
        if name not in data["writers_names"] and name != "N/A":
            data["writers_names"].append(name) 
            data["writers"].append({"id" : writer.person_id.id, "name" : name})
    return data

def extract_movies() -> dict:
    movies = []
    bar = Bar('Processing', max=Movie.objects.count())
    for movie in Movie.objects.all():
        movies.append(movie_to_dict(movie))
        bar.next()
    bar.finish()
    return movies

def load_movies_es(movies: list):
    url = f"{settings.BASE_ES_URL}_bulk?filter_path=items.*.error"
    headers = {
        'Content-Type': 'application/x-ndjson'
    }
    payload = ""

    for id, movie in enumerate(movies, start=1):
        payload+=json.dumps(
            {"index": {"_index": "movies", "_id": id}}
        ) + "\n" + json.dumps(movie) + "\n"

    requests.request("POST", url, headers=headers, data=payload)

def is_database_synchronized(database):
    connection = connections[database]
    connection.prepare_database()
    executor = MigrationExecutor(connection)
    targets = executor.loader.graph.leaf_nodes()
    return not executor.migration_plan(targets)

class Command(BaseCommand):
    help = 'Load data from SQLite database to PostgreSQL and to elasticsearch'

    def handle(self, *args, **options):
        init_es()
        if is_database_synchronized(DEFAULT_DB_ALIAS):
            load_movies_es(extract_movies())
            return
        else:
            raise BadMigrationError("Unapplied migrations found.")
