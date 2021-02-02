import json

from peewee import *
from playhouse import shortcuts

from pathlib import Path

database = SqliteDatabase(Path(__file__).parent / 'yandex_files/sqlite_yandex_db.sqlite')

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database
    
    @classmethod
    def get_names(cls) -> str:
        """Method that get names in Actors or in Writers class

        Raises:
            NameError: raise exception if mathod execute not in Actors or Writers class

        Yields:
            str: name of writer or actor
        """
        if cls.__name__ in ['Actors', 'Writers']:
            query = cls.select(cls.name.distinct()).execute()
            for writer in query:
                yield writer.name
        else:
            raise NameError("This method allows only in Actors and Writers class")

class Actors(BaseModel):
    """
    Model that contains information about people that take a role in film like actors
    """
    name = TextField(null=True)

    class Meta:
        table_name = 'actors'

class MovieActors(BaseModel):
    """
    This table store data about what people take a role in what film
    """
    actor_id = TextField(null=True)
    movie_id = TextField(null=True)

    class Meta:
        table_name = 'movie_actors'
        primary_key = False
    


class Movies(BaseModel):
    """
    Representation the information about film
    """
    director = TextField(null=True)
    genre = TextField(null=True)
    id = TextField(null=True, primary_key=True)
    imdb_rating = TextField(null=True)
    plot = TextField(null=True)
    ratings = TextField(null=True)
    title = TextField(null=True)
    writer = TextField(null=True)
    writers = TextField(null=True)

    class Meta:
        table_name = 'movies'
    
    @classmethod
    def get_directors(cls):
        return [movie.director for movie in cls.select(cls.director).distinct().execute()]

    def to_dict(self):
        """
        Transefer PeeweeQuerySet for class Movie in the dict with some modifications like 
        """
        data = shortcuts.model_to_dict(self)
        data['director'] = data.get('director').replace(", ", ",").split(',') if data.get('director') != "N/A" else ""
        data['genre'] = data.get('genre').replace(", ", ",").split(',')
        try:
            data['writers'] = json.loads(data.get('writers'))
        except json.decoder.JSONDecodeError:
            pass
        data['imdb_rating'] = data.get('imdb_rating') if data.get('imdb_rating') != "N/A" else 0.0
        return data

    def get_actors(self):
        """
        Return all actor names that take a roles in this film
        """
        for actor in MovieActors.select(Actors).join(Actors, on=(Actors.id == MovieActors.actor_id)).where(MovieActors.movie_id == self.id):
            yield actor.actors.name
    
    def get_writers(self):
        """
        Return all writer names that take a roles in this film
        """
        if self.writers:
            for writer in json.loads(self.writers):
                yield Writers.get(id=writer.get('id')).name
        else:
            yield Writers.get(id=self.writer).name
    

            

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

    class Meta:
        table_name = 'writers'

class People:
    """
    Representation information about all people (writers, actors )
    """
    @staticmethod
    def all_person():
        person={writer_name for writer_name in Writers.get_names()}\
            .union({actor_name for actor_name in Actors.get_names()})\
            .union({director_name for director_name in Movies.get_directors()})
        for people in person:
            if people == "N/A":
                continue
            yield people

# print(Movies.get_directors())