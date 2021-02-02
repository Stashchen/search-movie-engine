# Django API
API, that fetch movie data form ElasticSearch

## API reference
---
### **GET** api/movies/

*Description:* 

Fetch data about all movies. Movies can be filtered by 
* limit
* page
* sort (with sort order)
* search, that finde any full-text matches, based on the title

*Return format:*

``` js
{
    "id": movie_id,
    "title": movie_title,
    "imdb_rating": movie_rating
}
```

---
### **GET** api/movies/{movie_id}

*Description:* 

Fetch one movie detailed data

*Return format:*

``` js
{
  "id": movie_id,
  "title": movie_title,
  "imdb_rating": movie_rating,
  "description": movie_description,
  "genre": movie_genre,
  "actors": [],
  "writers": [],
  "director": movie_director
}
```

❗ For more details about using current api paste *<span style="text-decoration: underline;">api-schema.yaml</span>* file into [OpenApi/Swagger Editor](https://editor.swagger.io/)❗

## Environmental variables
All the variables are described in *<span style="text-decoration: underline;">.env.example</span>* file

## Run API
1. Create virtual environment
```
python -m venv env
. ./env/bin/activate  # For linux
. ./env/Script/activate  # For Windows
```
2. Install dependencies
```
pip install -r requirements.txt
```
3. Create *.env* file, based on *.env.example*
4. Run server
```
cd search_movie_engine
python manage.py runserver
```