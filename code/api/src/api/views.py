import logging
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView

from pprint import pprint
from .forms import MoviesSearchForm, DEFAULT_MOVIES_FORM_INITIALS

from .logic.es_handler import search_movies

logger = logging.getLogger(__name__)


class MovieList(APIView):

    def get(self, request, format=None):

        data = DEFAULT_MOVIES_FORM_INITIALS.copy()
        data.update({key: value for key, value in request.GET.items()})

        form = MoviesSearchForm(data)  # For is used to check validation of the params

        if not form.is_valid():
            for error in form.errors.values():
                logger.error(', '.join(error))
            return Response(status=400)
        
        movies = search_movies(data)

        pprint(movies)

        return Response(status=200)