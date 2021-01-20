from dataclasses import dataclass
from typing import List


@dataclass
class Actor:
    id: int
    name: str

    def to_dict(self) -> dict:
        return {
            'id': int(self.id),
            'name': self.name,
        }

@dataclass
class Writer:
    id: str
    name: str

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
        }

@dataclass
class ShortMovie:
    id: str
    title: str
    imdb_rating: float

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'imdb_rating': self.imdb_rating,
        }

@dataclass
class Movie(ShortMovie):
    description: str
    genre: List[str]
    actors: List[Actor]
    writers: List[Writer]
    directors: List[str]

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            'description': self.description,
            'genre': self.genre,
            'actors': [a.to_dict() for a in self.actors],
            'writers': [w.to_dict() for w in self.writers],
            'director': self.directors,
        }