from django.core import serializers
from django.conf import settings

from urllib.parse import urljoin

import json
import requests


def add_movie_es(movie, writers, actors):
    actors_json = json.loads(serializers.serialize("json", actors))
    writers_json = json.loads(serializers.serialize("json", writers))
    movie_json = json.loads(serializers.serialize("json", [movie]))[0]
    movie_dict = {
        "id" : movie_json.get('pk'),
        **movie_json.get('fields'),
        "actors_names" : [
            actor.get('fields').get('name') for actor in actors_json
        ],
        "actors" : [
            {
                "id" : actor.get("pk"), 
                "name" : actor.get('fields').get('name')
            } for actor in actors_json],
        "writers_names" : [
            writer.get('fields').get('name') for writer in writers_json
        ],
        "writers" : [
            {
                "id" : writer.get("pk"), 
                "name" : writer.get('fields').get('name')
            } for writer in writers_json]
    }
    movie_dict['description'] = movie_dict.pop('plot')
    
    requests.post(
        url=urljoin(settings.BASE_ES_URL, 'movies/_doc'),
        data=json.dumps(movie_dict),
        headers={'Content-Type': 'application/json'}
    )
