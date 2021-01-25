import requests
import json

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.migrations.executor import MigrationExecutor
from django.db import connections, DEFAULT_DB_ALIAS
from django.forms.models import model_to_dict
from progress.bar import Bar
from requests.models import Request
from api.models import (
    Movies,
    MovieActors,
    MovieWriters
)

def init_es() -> Request():
    url = f"{settings.BASE_ES_URL}movies"

    payload="""
        {
        "settings": {
            "refresh_interval": "1s",
            "analysis": {
            "filter": {
                "english_stop": {
                "type":       "stop",
                "stopwords":  "_english_"
                },
                "english_stemmer": {
                "type": "stemmer",
                "language": "english"
                },
                "english_possessive_stemmer": {
                "type": "stemmer",
                "language": "possessive_english"
                },
                "russian_stop": {
                "type":       "stop",
                "stopwords":  "_russian_"
                },
                "russian_stemmer": {
                "type": "stemmer",
                "language": "russian"
                }
            },
            "analyzer": {
                "ru_en": {
                "tokenizer": "standard",
                "filter": [
                    "lowercase",
                    "english_stop",
                    "english_stemmer",
                    "english_possessive_stemmer",
                    "russian_stop",
                    "russian_stemmer"
                ]
                }
            }
            }
        },
        "mappings": {
            "dynamic": "strict",
            "properties": {
            "id": {
                "type": "keyword"
            },
            "imdb_rating": {
                "type": "float"
            },
            "genre": {
                "type": "keyword"
            },
            "title": {
                "type": "text",
                "analyzer": "ru_en",
                "fields": {
                "raw": { 
                    "type":  "keyword"
                }
                }
            },
            "description": {
                "type": "text",
                "analyzer": "ru_en"
            },
            "director": {
                "type": "text",
                "analyzer": "ru_en"
            },
            "actors_names": {
                "type": "text",
                "analyzer": "ru_en"
            },
            "writers_names": {
                "type": "text",
                "analyzer": "ru_en"
            },
            "actors": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                "id": {
                    "type": "keyword"
                },
                "name": {
                    "type": "text",
                    "analyzer": "ru_en"
                }
                }
            },
            "writers": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                "id": {
                    "type": "keyword"
                },
                "name": {
                    "type": "text",
                    "analyzer": "ru_en"
                }
                }
            }
            }
        }
        }
    """
    headers = {
    'Content-Type': 'application/json'
    }

    return requests.request("PUT", url, headers=headers, data=payload)


def extract_movies() -> dict:
    movies = []
    bar = Bar('Processing', max=Movies.objects.count())
    for movie in Movies.objects.all():
        data = {}
        data.update(model_to_dict(movie))
        data["actors_names"] = []
        data["actors"] = []
        for actor in MovieActors.objects.filter(movie_id=movie):
            actor_name = actor.actor.name
            if actor_name != "N/A":
                data["actors_names"].append(actor_name)
                data["actors"].append({"id" : actor.actor.id, "name" : actor_name})
        data["writers_names"] = []
        data["writers"] = []
        writers = MovieWriters.objects.filter(movie=movie)
        for writer in writers:
            name = writer.writer.name
            if name not in data["writers_names"] and name != "N/A":
                data["writers_names"].append(name) 
                data["writers"].append({"id" : writer.writer.id, "name" : name})
        movies.append(data)
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
        if init_es().status_code == 200:
            if is_database_synchronized(DEFAULT_DB_ALIAS):
                print('All migrations have been applied.')
                load_movies_es(extract_movies())
                print("All data is transfered to elasticsearch")
            else:
                print("Unapplied migrations found.")