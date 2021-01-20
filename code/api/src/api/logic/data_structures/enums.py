from enum import Enum


class SortField(Enum):
    ID = 'id'
    TITLE = 'title'
    IMDB_RATING = 'imdb_rating'

class SortOrder(Enum):
    ASC = 'asc'
    DESC = 'desc'