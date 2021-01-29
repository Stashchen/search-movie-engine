import requests
import mock
import sys

from io import StringIO

from django.urls import path, reverse, include
from django.test import TestCase, Client
from django.core.management import call_command
from django.db.migrations.exceptions import BadMigrationError

from rest_framework.test import APITestCase

from api.logic.data_structures.enums import Positions
from api.models import Movie, Person, PersonPosition, Genre
from api.management.commands._sqlite_models import *


def fail_init_es():
    raise requests.exceptions.ConnectionError


class Test(TestCase):
    fixtures = ['init_data.json']

    def setUp(self) -> None:
        # self.client = RequestsClient()
        return super().setUp()

    def test_command_sqlite_to_postgres(self):
        call_command('sqlite_to_postgres')
        self.assertEqual(Movie.objects.count(), 999)

    @mock.patch('api.management.commands.etl.init_es', fail_init_es)
    def test_command_etl_failure(self):
        self.assertRaises(requests.exceptions.ConnectionError, call_command, "etl")

    def test_command_etl(self):
        self.assertEqual(call_command('etl'), None)

    @mock.patch('api.management.commands.etl.is_database_synchronized', return_value=False)
    def test_command_etl_no_migrations(self, mock_migrations):
        self.assertRaises(BadMigrationError, call_command, 'etl')

    def test_person(self):
        self.assertEqual(Person.objects.count(), 4133)
        self.assertEqual(Person.objects.filter(name="N/A").count(), 0)

    def test_movie(self):
        self.assertEqual(Movie.objects.count(), 999)
        self.assertEqual(Movie.objects.count(), 999)
        self.assertEqual(Movie.objects.filter(imdb_rating=0).count(), 1)
    
    def test_person_position(self):
        self.assertEqual(PersonPosition.objects.filter(position=Positions.DIRECTOR).count(), 705)
        self.assertEqual(PersonPosition.objects.filter(position=Positions.ACTOR).count(), 3401)
        self.assertEqual(PersonPosition.objects.filter(position=Positions.WRITER).count(), 1561)

    def test_genre(self):
        self.assertEqual(Genre.objects.count(), Genre.objects.distinct().count())


class ApiTest(APITestCase):
    fixtures = ['init_data.json']

    # def setUp(self) -> None:
    #     return super().setUp()

    def test_get_movies(self):
        response = self.client.get('/api/movies/', {'limit' : Movie.objects.count()}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), Movie.objects.count())
    
    @mock.patch('api.forms.MoviesSearchForm.is_valid', return_value=False)
    @mock.patch('api.views._validation_errors_to_dict', return_value={"error" : "errors"})
    def test_bad_get_movies(self, mock_is_valid, mock_erros):
        response = self.client.get('/api/movies/', {'limit' : Movie.objects.count()}, format='json')
        self.assertEqual(response.status_code, 422)

    def test_post_movies(self):
        url = '/api/movies/'
        response = self.client.post(url, 
            {
                "id": "efremove21",
                "title": "Efremov",
                "description": "Mr Plinkett discusses his views and personal feelings on The Force Awakens and the current state of the Star Wars franchise.",
                "imdb_rating": 8,
                "genre": [
                    "Action"
                ],
                "crew": [
                    {
                        "person_id" :"Mike Stoklasa",
                        "position": "WRT"
                    }
                ]
            },
            format='json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Movie.objects.count(), 1000)
    
    def test_bad_post_movies(self):
        url = '/api/movies/'
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_get_movie_id(self):
        movie = Movie.objects.first()
        url = f'/api/movies/{movie.id}/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('title'), movie.title)

    def test_bad_get_movie_id(self):
        url = f'/api/movies/BAD_MOVIE_ID/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 404)

    @mock.patch("api.logic.es.es_requests.get_es_object_id", return_value=111)
    def test_put_movie_id(self, mock_es):
        movie = Movie.objects.first()
        url = f'/api/movies/{movie.id}/'
        response = self.client.put(url,
            {
                "id": movie.id,
                "title": "Efremov",
                "description": "Mr Plinkett discusses his views and personal feelings on The Force Awakens and the current state of the Star Wars franchise.",
                "imdb_rating": 8,
                "genre": [
                    "Action"
                ],
                "crew": [
                    {
                        "person_id" :"Mike Stoklasa",
                        "position": "WRT"
                    }
                ]
            },
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Movie.objects.get(id=movie.id).title, 'Efremov')

    def test_put_404_movie_id(self):
        url = '/api/movies/BAD_MOVIE_ID/'
        response = self.client.put(url, {}, format='json')
        self.assertEqual(response.status_code, 404)

    def test_put_400_movie_id(self):
        movie = Movie.objects.first()
        url = f'/api/movies/{movie.id}/'
        response = self.client.put(url, {}, format='json')
        self.assertEqual(response.status_code, 400)

    @mock.patch("api.logic.es.es_requests.get_es_object_id", return_value=111)
    def test_delete_movie_id(self, mock_es):
        old_movie_count = Movie.objects.count()
        movie = Movie.objects.first()
        url = f'/api/movies/{movie.id}/'
        response = self.client.delete(url, format='json')
        new_movie_count = Movie.objects.count()
        self.assertEqual(response.status_code, 204)
        self.assertEqual(new_movie_count, (old_movie_count - 1))

    def test_delete_404_movie_id(self):
        url = f'/api/movies/BAD_MOVIE_ID/'
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, 404)

    
