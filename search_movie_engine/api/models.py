from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .logic.data_structures.enums import Positions


class Person(models.Model):
    """
    Any people who take part in creating movie.
    """
    name = models.CharField("Name", max_length=50)

    def __str__(self): # pragma: no cover
        return self.name
    
class Movie(models.Model):
    """
    Represents movie object.
    """
    id = models.CharField("Id", max_length=36, primary_key=True)
    title = models.CharField("Title", max_length=100)
    description = models.TextField("Description", max_length=1500)
    imdb_rating = models.FloatField("Rating", validators=[MinValueValidator(0), MaxValueValidator(10)])
    crew = models.ManyToManyField("Person", verbose_name="Movie crew", through='PersonPosition')
    genre = models.ManyToManyField("Genre", verbose_name="Genres")

    def __str__(self): # pragma: no cover
        return self.title
    
class PersonPosition(models.Model):
    """
    Through db table that stores Movies crews jobs.
    """
    movie_id = models.ForeignKey("Movie", verbose_name="Movie ID", on_delete=models.CASCADE)
    person_id = models.ForeignKey("Person", verbose_name="Person ID", on_delete=models.CASCADE)
    position = models.CharField("Position", max_length=3, choices=Positions.choices)

class Genre(models.Model):
    """
    Movie genres table.
    """
    name = models.CharField("Name", max_length=50)

    def __str__(self): # pragma: no cover
        return self.name
    