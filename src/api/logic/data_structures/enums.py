from django.db import models 
from enum import Enum


class SortField(Enum):
    ID = 'id'
    TITLE = 'title'
    IMDB_RATING = 'imdb_rating'

class SortOrder(Enum):
    ASC = 'asc'
    DESC = 'desc'

class Positions(models.TextChoices):
    WRITER = 'WRT', 'Writer'
    ACTOR = 'ACT', 'Actor'
    DIRECTOR = 'DCT', 'Director' 
