import logging
from django.shortcuts import render
from django.http import JsonResponse

from typing import List

from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from .logic.parse_func import parse_movies_get_params
from .forms import MoviesSearchForm

from .logic.es_handler import get_movies_list, get_movie_by_id


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


class MoveDetails(APIView):
    """
    View, that is invoked by `movies/{movieID}` path
    """
    def get(self, request, movieID, format=None):
        
        movie = get_movie_by_id(movieID)

        if movie is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        return Response(movie.to_dict())