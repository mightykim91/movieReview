from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=30)

class Movie(models.Model):
    title = models.CharField(max_length=100)
    original_title = models.CharField(max_length=100)
    release_date = models.DateTimeField()
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    adult = models.BooleanField()
    overview = models.TextField()
    original_language = models.CharField(max_length=20)
    poster_path = models.CharField(max_length=200)
    backdrop_path = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre, related_name='movies')