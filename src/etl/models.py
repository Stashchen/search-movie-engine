import os

from playhouse.postgres_ext import PostgresqlExtDatabase
from peewee import Model
from peewee import TextField, IntegerField, ForeignKeyField
from dotenv import load_dotenv

load_dotenv()


sqlite_db = PostgresqlExtDatabase(
    os.getenv("DB_NAME"),
    user = os.getenv("USER_DB"),
    password = os.getenv("PASSWORD_DB"),
    host = os.getenv("HOST_DB"),
    port = os.getenv("PORT_DB")
)

class BaseModel(Model):
    """A base model that will use our Sqlite database."""
    class Meta:
        database = sqlite_db

class Actors(BaseModel):
    """A model that defines `actors` table\n
    [fields:]\n
    id, name"""
    id = IntegerField(primary_key=True, column_name='id')
    name = TextField(column_name='name')

    class Meta:
        table_name = 'actors'

class Movies(BaseModel):
    """A model that use `movies` table from yandex_db\n
    [fields]:\n
    id, genre, director, writer, title, plot, ratings, imdb_rating, writers"""
    id = TextField(primary_key=True, column_name='id')
    genre = TextField(column_name='genre')
    director = TextField(column_name='director')
    writer = TextField(column_name='writer')
    title = TextField(column_name='title')
    plot = TextField(column_name='plot')
    ratings = TextField(column_name='ratings')
    imdb_rating = TextField(column_name='imdb_rating')
    writers = TextField(column_name='writers')

    class Meta:
        table_name = 'movies'

class Movie_actors(BaseModel):
    """
    A model that contain 2 Foreign_key for 2 models\n
    `movie_id` refer to `movies` talbe\n
    `actor_id` refer to `actors` table\n
    [fields]:\n
    movie_id, actor_id
    """
    movie_id = ForeignKeyField(Movies)
    actor_id = ForeignKeyField(Actors)

    class Meta:
        table_name = 'movie_actors'

class Writers(BaseModel):
    """A model that defines `writers` table\n
    [fields]:\n
    id, name"""
    id = TextField(primary_key=True, column_name='id')
    name = TextField(column_name='name')

    class Meta:
        table_name = 'writers'