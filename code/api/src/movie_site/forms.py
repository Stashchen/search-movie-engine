from django import forms
from django.forms import CharField, IntegerField, TextField

"""{
    "id": "tt0121766",
    "imdb_rating": 7.5,
    "genre": "Action, Adventure, Fantasy, Sci-Fi",
    "title": "Star Wars: Episode III - Revenge of the Sith",
    "description": "Near the end of the Clone Wars, Darth Sidious has revealed himself and is ready to execute the last part of his plan to rule the galaxy. Sidious is ready for his new apprentice, Darth Vader, to step into action and kill the remaining Jedi. Vader, however, struggles to choose the dark side and save his wife or remain loyal to the Jedi order.",
    "director": "George Lucas",
    "actors_names": [
        "Ewan McGregor",
        "Natalie Portman",
        "Hayden Christensen",
        "Ian McDiarmid"
    ],
    "actors": [
        {
            "id": 8,
            "name": "Ewan McGregor"
        },
        {
            "id": 9,
            "name": "Natalie Portman"
        },
        {
            "id": 11,
            "name": "Hayden Christensen"
        },
        {
            "id": 12,
            "name": "Ian McDiarmid"
        }
    ],
    "writers_names": [
        "George Lucas"
    ],
    "writers": [
        {
            "id": "0b60f2f348adc2f668a9a090165e24f3d3a7cf5a",
            "name": "George Lucas"
        }
    ]
"""

class Movie(forms.Form):
    id = CharField(max_length=9, required=True)
    imdb_rating = IntegerField(min_value=0.0, max_value=10.0, required=True)
    genre = CharField(max_length=250, required=True)
    title = CharField(max_length=250, required=True)
    description = TextField()
    director = CharField(max_length=250)