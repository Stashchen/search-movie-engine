import json
from peewee import *

database = SqliteDatabase('/home/mikita/Repositories/search-movie-engine/db.sqlite')

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Actors(BaseModel):
    name = TextField(null=True)

    class Meta:
        table_name = 'actors'


class Movies(BaseModel):
    director = TextField(null=True)
    genre = TextField(null=True)
    id = TextField(null=True, primary_key=True)
    imdb_rating = TextField(null=True)
    plot = TextField(null=True)
    ratings = TextField(null=True)
    title = TextField(null=True)
    writer = TextField(null=True)
    writers = TextField(null=True)

    def to_dict(self):
        return {
            "id" : self.id,
            "imdb_rating" : float(self.imdb_rating) if self.imdb_rating != ("N/A") else None,
            "genre" : self.genre,
            "title" : self.title,
            "description" : self.plot if self.plot != "N/A" else None,
            "director" : self.director if self.director != "N/A" else None
        }

    def get_writers(self):
        return [writer.get("id") for writer in json.loads(self.writers)] if self.writers else [self.writer]


    @classmethod
    def count(cls) -> int:
        return cls.select().count()

    class Meta:
        table_name = 'movies'

class MovieActors(BaseModel):
    movie_id = ForeignKeyField(Movies)
    actor_id = ForeignKeyField(Actors)

    class Meta:
        table_name = 'movie_actors'
        primary_key = False

class RatingAgency(BaseModel):
    id = TextField(null=True)
    name = TextField(null=True)

    class Meta:
        table_name = 'rating_agency'
        primary_key = False

class SqliteSequence(BaseModel):
    name = BareField(null=True)
    seq = BareField(null=True)

    class Meta:
        table_name = 'sqlite_sequence'
        primary_key = False

class Writers(BaseModel):
    id = TextField(null=True, primary_key=True)
    name = TextField(null=True)

    @classmethod
    def get_name(cls, id) -> str:
        return cls.get(cls.id == id).name

    class Meta:
        table_name = 'writers'

# print(
#     [movie.get_writers() for movie in Movies.select().execute()]
# )