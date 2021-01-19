import requests
import json
from progress.bar import Bar
from models import Actors, Movies, Movie_actors, Writers

"""{
    "id": "my pretty text",
    "imdb_rating": 15,
    "genre" : "StarWars",
    "title" : "qwert",
    "description" : "something interesting",
    "director" : "George Lucas",
    "actors_names" : ["qeqweqweqw", "nik"],
    "writers_names" : ["werewrwer"],
    "actors" : [
        {"id": "t0123qwe", "name" : "Nikita Efremov"},
        {"id": "t023", "name" : "Georg"}
    ],
    "writers" : [
        {"id" : "123123", "name" : "Daniil Lapezo"}
    ]
}"""

def extract_movies() -> dict:
    movies = []
    bar = Bar('Processing', max=Movies.select().count())
    for movie in Movies.select().execute():
        data = {}
        data["id"] = movie.id
        data["imdb_rating"] = float(movie.imdb_rating) if movie.imdb_rating != ("N/A") else None
        data["genre"] = movie.genre
        data["title"] = movie.title
        data["description"] = movie.plot if movie.plot != "N/A" else None
        data["director"] = movie.director if movie.director != "N/A" else None
        data["actors_names"] = []
        data["actors"] = []
        for actor in Movie_actors.select(Movie_actors.actor_id).join(Actors).where(Movie_actors.movie_id == movie.id):
            actor_name = actor.actor_id.name
            if actor_name != "N/A":
                data["actors_names"].append(actor_name)
                data["actors"].append({"id" : actor.actor_id.id, "name" : actor_name})
        data["writers_names"] = []
        data["writers"] = []
        if movie.writers:
            for writer in json.loads(movie.writers):
                name_query = Writers.get(Writers.id == writer.get("id")).name
                if name_query not in data["writers_names"] and name_query != "N/A":
                    data["writers_names"].append(Writers.get(Writers.id == writer.get("id")).name) 
                    data["writers"].append({"id" : writer.get("id"), "name" : Writers.get(Writers.id == writer.get("id")).name})
        else:
            name_query = Writers.get(Writers.id == movie.writer).name
            if name_query != "N/A":
                data["writers_names"].append(name_query)
                data["writers"].append({"id" : movie.writer, "name" : name_query})
        movies.append(data)
        bar.next()
    bar.finish()
    return movies

def load_movies(movies: list):
    url = "http://127.0.0.1:9200/_bulk?filter_path=items.*.error"
    headers = {
        'Content-Type': 'application/x-ndjson'
    }
    payload = ""
    for id, movie in enumerate(movies, start=1):
        payload+=json.dumps(
            {"index": {"_index": "movies", "_id": id}}
        ) + "\n" + json.dumps(movie) + "\n"

    requests.request("POST", url, headers=headers, data=payload)


if __name__ == "__main__":
    load_movies(extract_movies())
    print("All data is transfered")
