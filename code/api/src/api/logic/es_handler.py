# Hanlder for elastic search
import requests
from django.conf import settings
from dataclasses import dataclass

from typing import List

from urllib.parse import urljoin

from api.enums import SortField

from api.logic.data_classes import (
   Actor, Writer, ShortMovie, Movie
)


def search_movies(req_params: dict):
   """
   :param req_params  Get request query params

   :return movies
   """
   
   sort_value = req_params.get('sort')
   limit = req_params.get('limit')

   if sort_value == SortField.TITLE.value:
      sort_value = f'{sort_value}.raw'


   es_request_data = {
      'size': limit,
      'from': (req_params.get('page') - 1) * limit,
      'sort': [
         {
            sort_value: req_params.get('sort_order')
         }
      ],
      '_source': ['id', 'title', 'imdb_rating'], 
   }

   search_query = req_params.get('search')

   if search_query:
      es_request_data['query'] = {
         'multi_match': {
               'query': search_query,
               'fuzziness': 'auto',
               'fields': [
                  'title^5',
                  'description^4',
                  'genre^3',
                  'actors_names^3',
                  'writers_names^2',
                  'director'
               ]
         }
      }

   response = requests.get(
      url=urljoin(settings.BASE_ES_URL, 'movies/_search'),
      json=es_request_data,
      headers={'Content-Type': 'application/json'}
   )

   if not response.ok:
      response.raise_for_status()

   data = response.json()
   result = data['hits']['hits']
   movies = []

   if movies:
      for record in result:
         movie_raw = record.get('_source')
         movies.append(ShortMovie(
            id=movie_raw.get('id'),
            title=movie_raw.get('title'),
            imdb_rating=movie_raw.get('imdb_rating')
         ))
   
   return movies