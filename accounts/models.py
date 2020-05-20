from django.db import models
from movies.models import Movie
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class User(AbstractUser):


    like_movies = models.ManyToManyField(
        Movie,
        related_name='like_users'
    )

