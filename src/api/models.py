# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from pprint import pprint

class Actors(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()

    def __str__(self):
        return self.name
        
    class Meta:
        db_table = 'actors'


class Writers(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'writers'


class Movies(models.Model):
    id = models.TextField(primary_key=True)
    genre = models.TextField(blank=True, null=True)
    director = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    imdb_rating = models.TextField(blank=True, null=True)
    
    writers = models.ManyToManyField(Writers)
    actors = models.ManyToManyField(Actors)
    class Meta:
        db_table = 'movies'
