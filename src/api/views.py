import logging

from typing import List

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .logic.parse_func import parse_movies_get_params
from .forms import MoviesSearchForm
from .models import Movies

from api.management.commands.etl import movie_to_dict

from .logic.es import es_requests
from .logic.es.views import get_movies_list, get_movie_by_id

from .serializers import MoviesSerializer

def _process_es_and_django_funcs(django_func, es_func, django_params={}, es_params={}) -> None:
    """
    Check that both: django and es func pass.

    :param django_func: django functionality
    :param es_func: ElasticSearch functionality
    """
    try:
        movie = django_func(**django_params)
        es_params['request_data'] = movie_to_dict(movie)
        es_func(**es_params)
    except Exception as e:
        logging.error(e)

def _validation_errors_to_dict(errors: dict) -> List[dict]:
    validation_errors = []
    for field_name, field_errors in errors.items():
        for err in field_errors:
            validation_errors.append(
                {
                    'loc': [
                        'query',
                        field_name,
                    ],
                    'msg': err
                },
            )
    return validation_errors  

class MovieList(APIView):
    """
    View, that is invoked by `movies/` path
    """
    def get(self, request, format=None):

        form_data = parse_movies_get_params(request)

        form = MoviesSearchForm(form_data)  # For is used to check validation of the params

        validation_errors = []
        if not form.is_valid():            
            validation_errors = _validation_errors_to_dict(form.errors)

        if validation_errors:
            return Response(validation_errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        movies = get_movies_list(form_data)

        return Response(data=[movie.to_dict() for movie in movies])

    def post(self, request, format=None):
        # Add new movie
        serializer = MoviesSerializer(data=request.data)
        
        if serializer.is_valid():
            _process_es_and_django_funcs(
                django_func=serializer.save,  # Save into db
                es_func=es_requests.post,  # Send data to ES
                es_params={
                    'es_index': 'movies'
                }
            )
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class MoveDetails(APIView):
    """
    View, that is invoked by `movies/{movieID}` path
    """
    def get(self, request, movieID, format=None):
        movie = get_movie_by_id(movieID)

        if movie is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        return Response(movie.to_dict())

    def put(self, request, movieID, format=None):
        try:
            movie = Movies.objects.get(id=movieID)
        except Movies.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MoviesSerializer(instance=movie, data=request.data)
        if serializer.is_valid():
            _process_es_and_django_funcs(
                django_func=serializer.save,  # Save into db
                es_func=es_requests.put,  # Update data in ES
                es_params={
                    'es_index': 'movies',
                    'es_id': es_requests.get_es_object_id('movies', {'id': movieID})
                }
            )
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, movieID, format=None):
        try:
            movie = Movies.objects.get(id=movieID)
        except Movies.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        _process_es_and_django_funcs(
            django_func=movie.delete,
            es_func=es_requests.delete,
            es_params={
                'es_index': 'movies',
                'request_data': {},
                'es_id': es_requests.get_es_object_id('movies', {'id': movieID})
            }
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
