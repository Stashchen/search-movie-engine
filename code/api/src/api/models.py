# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Actors(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'actors'
    


class MovieActors(models.Model):
    movie = models.ForeignKey('Movies', models.DO_NOTHING)
    actor = models.ForeignKey(Actors, models.DO_NOTHING, blank=True, null=True)
    id = models.IntegerField(primary_key=True)

    class Meta:
        db_table = 'movie_actors'


class MovieWriters(models.Model):
    id = models.IntegerField(primary_key=True)
    movie = models.ForeignKey('Movies', models.DO_NOTHING)
    writer = models.ForeignKey('Writers', models.DO_NOTHING)

    class Meta:
        db_table = 'movie_writers'


class Movies(models.Model):
    id = models.TextField(primary_key=True)
    genre = models.TextField(blank=True, null=True)
    director = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    plot = models.TextField(blank=True, null=True)
    imdb_rating = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'movies'


class Writers(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'writers'
