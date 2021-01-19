import logging
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView

from pprint import pprint
from .forms import MoviesSearchForm, DEFAULT_MOVIES_INITIALS

from .logic.es_handler import search_movies

logger = logging.getLogger(__name__)


class MovieList(APIView):

    def get(self, request, format=None):

        data = DEFAULT_MOVIES_INITIALS.copy()
        data.update({key: value for key, value in request.GET.items()})

        form = MoviesSearchForm(data)

        if not form.is_valid():
            for error in form.errors.values():
                logger.error(', '.join(error))
            return Response(400)
        
        search_movies(data)

        return Response(200)