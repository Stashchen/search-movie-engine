from django.conf import settings
from dataclasses import dataclass

from typing import List, Union
from urllib.parse import urljoin

from api.logic.data_structures.enums import SortField
from api.logic.data_structures.data_classes import (
   Actor, Writer, ShortMovie, Movie
)
from api.logic.es import es_requests


def get_movies_list(request_params: dict) -> List[ShortMovie]:
   """
   :param request_params: Get request query params

   :return: List of movies, grabed with ElasticSearch
   """

   sort_value = request_params.get('sort')
   sort_order = request_params.get('sort_order')
   limit = int(request_params.get('limit'))
   page = int(request_params.get('page'))

   if sort_value == SortField.TITLE.value:
      sort_value = f'{sort_value}.raw'  # Format .raw for ElasticSearch 

   request_data = {
      'size': limit,
      'from': (page - 1) * limit,
      'sort': [
         {
            sort_value: sort_order
         }
      ],
      '_source': ['id', 'title', 'imdb_rating'], 
   }

   # Parse string query and create request for the ElasticSearch
   search_query = request_params.get('search')

   if search_query:
      request_data['query'] = {
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

   response = es_requests.get('movies', request_data)

   if not response.ok:
      response.raise_for_status()

   data = response.json()
   result = data['hits']['hits']
   movies = []

   for record in result:
      movie_raw = record.get('_source')
      movies.append(ShortMovie(
         id=movie_raw.get('id'),
         title=movie_raw.get('title'),
         imdb_rating=movie_raw.get('imdb_rating')
      ))
   
   return movies

def get_movie_by_id(id: str) -> Union[Movie, None]:
   """
   :param id: Selected movie id

   :return: Selected movie details or None
   """
   request_data = {
      'query': {
         'term': {
               'id': {
                  'value': id
               }
         }
      }
   }
    
   response = es_requests.get('movies', request_data)

   if not response.ok:
      response.raise_for_status()

   data = response.json()

   result = data['hits']['hits']

   if not result:
      return None

   movie_raw = result[0]['_source']
   movie = Movie(
      id=movie_raw['id'],
      title=movie_raw['title'],
      imdb_rating=movie_raw['imdb_rating'],
      description=movie_raw['description'],
      genre=movie_raw['genre'],
      actors=[Actor(**x) for x in movie_raw['actors']],
      writers=[Writer(**x) for x in movie_raw['writers']],
      directors=movie_raw['director']
   )
   return movie