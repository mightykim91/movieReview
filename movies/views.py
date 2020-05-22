from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Movie
import random
from random import shuffle


# Create your views here.
def index(request):
    movies = Movie.objects.all()
    paginator = Paginator(movies, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    #장르 추출
    genres = set()
    recommendation = []
    if request.user.is_authenticated:
        user = request.user
        like_movies = user.like_movies.all()

        for movie in like_movies:
            for genre in list(movie.genres.all().values('name')):
                genres.add(genre['name'])

        #추천
        not_watched = []

        for movie in movies:
            if movie not in user.like_movies.all():
                not_watched.append(movie)


        while len(recommendation) < 10:
            rand_int = random.randrange(len(movies)-len(not_watched))
            shuffle(not_watched)
            not_watched_movie_genres = []
            for j in list(not_watched[rand_int].genres.all().values('name')):
                not_watched_movie_genres.append(j['name'])

            for temp_genre in not_watched_movie_genres:
                if temp_genre in genres:
                    recommendation.append(not_watched[rand_int])
                    break

    context = {
        'movies':movies,
        'page_obj':page_obj,
        'recom_top_five': recommendation[:5],
        'recom_bot_five': recommendation[5:],
    }


    return render(request, 'movies/index.html', context)


def detail(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    user = request.user
    color = 'black'
    if user.is_authenticated:
        if user.like_movies.filter(pk=movie_pk).exists():
            color = 'crimson'

    genres = []
    for genre in list(movie.genres.all().values('name')):
        genres.append(genre["name"])

    context = {
        'title': movie.title,
        'release_date': movie.release_date,
        'popularity': movie.popularity,
        'adult': movie.adult,
        'vote_count': movie.vote_count,
        'vote_average': movie.vote_average,
        'overview': movie.overview,
        'genres': genres,
        'color': color,

    }
    return JsonResponse(context)


@login_required
def like(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)

    if movie.like_users.filter(pk=user.pk).exists():
        movie.like_users.remove(user)
        liked = False

    else:
        movie.like_users.add(user)
        liked = True
    context = {
        'liked':liked,
        'count':movie.like_users.count(),
    }

    return JsonResponse(context)

