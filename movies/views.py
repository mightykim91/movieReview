from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Movie
import operator
from random import shuffle

# Create your views here.
def index(request):
    movies = Movie.objects.all()
    paginator = Paginator(movies, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {

        'movies':movies,
        'page_obj':page_obj,
    }


    return render(request, 'movies/index.html', context)

def detail(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
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

    }
    return JsonResponse(context)

@login_required
def like(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)
    liked = False
    if movie.like_users.filter(pk=user.pk).exists():
        movie.like_users.remove(user)
    else:
        movie.like_users.add(user)
        liked = True
    context = {
        'liked':liked,
        'count':movie.like_users.count(),
    }

    return JsonResponse(context)

#recommendation
'''
@login_required
def recommend(request):
    user = request.user
    like_movies = user.like_movies.all().values('genre')
    genre_count = {}
    for genre in like_movies:
        if genre not in genre_count.keys():
           genre_count[genre] = 1
        else:
            genre_count[genre] += 1
    top_genres = sorted(genre_count.values(), key=operator.itemgetter(1))[:10]
    recommendation = []
    i = 0
    while i < 10:
        movies = Movie.objects.all().values('genres')
        shuffle(movies)
        random_index = range(0,movies.length)
        if movies[random_index] in top_genres:
            recommendation.append(movies[random_index])
            i += 1
        else:
            continue
    context = {
        "recommendation": recommendation,
    }

    return render(request, 'movies/index.html', context)
'''
