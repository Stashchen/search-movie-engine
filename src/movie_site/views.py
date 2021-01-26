from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import MovieForm
from .utils.add_movie_es import add_movie_es
from api.models import Movies, MovieWriters, MovieActors
from pprint import pprint

import requests

def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            id = f"tt{Movies.objects.count() + 1}"
            imdb_rating = form.cleaned_data['imdb_rating']
            genre = form.cleaned_data['genre']
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            actors = form.cleaned_data['actors']
            writers = form.cleaned_data['writers']
            movie = Movies.objects.create(
                id=id,
                imdb_rating=imdb_rating,
                genre=genre,
                title=title,
                plot=description,
            )
            
            for writer in writers:
                MovieWriters.objects.create(
                    movie=movie,
                    writer=writer
                )
            for actor in actors:
                MovieActors.objects.create(
                    movie=movie,
                    actor=actor
                )
            add_movie_es(movie, writers, actors)
            return HttpResponseRedirect('')
    movies = requests.get(
        'http://localhost:8000/api/movies'
    ).json()
    form = MovieForm()
    return render(request, 'movie_site/base.html', {'form' : form, 'movies' : movies})

# def search(request):
