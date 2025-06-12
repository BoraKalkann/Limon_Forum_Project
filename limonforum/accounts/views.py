from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import requests
from slugify import slugify
from .models import UserProfile
from forum.models import Comment
from django.contrib.auth import authenticate,login
from decouple import config

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username = username, password = password)
    
        if user is not None:
            login(request,user)
            return redirect('accounts:profilePage')
        
    return render(request, 'accounts/login.html')   
 
def register_view(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']

        user = User.objects.create_user(
            first_name = first_name,
            last_name = last_name,
            username = username,
            email = email,
            password = password,
        )
        user.save()
        return redirect('accounts:loginPage')  
    return render(request, 'accounts/register.html')

def profile_view(request):
    user = request.user

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        surname = request.POST.get("surname", "").strip()
        bio = request.POST.get("bio", "").strip()
        image = request.FILES.get("image")

        user.first_name = name
        user.last_name = surname
        user_profile, created = UserProfile.objects.get_or_create(user=user)

        if bio:
            user_profile.bio = bio
        if image:
            user_profile.image = image

        user_profile.save()
        user.save()

        return redirect("accounts:profilePage")

    user_profile, _ = UserProfile.objects.get_or_create(user=user)

    game_api_key = config('RAWG_API_KEY')
    game_comments = Comment.objects.filter(user=user, content_type='game').values_list('slug', flat=True).distinct()
    games = []
    for slug in game_comments:
        url = f"https://api.rawg.io/api/games/{slug}?key={game_api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            games.append({
                'title': data.get('name', ''),
                'slug': slug,
                'thumbnail': data.get('background_image', ''),
                'released': data.get('released', '')
            })

    book_comments = Comment.objects.filter(user=user, content_type='book').values_list('slug', flat=True).distinct()
    books = []
    for slug in book_comments:
        query = slug.replace('-', '+')
        url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{query}&maxResults=1"
        response = requests.get(url)
        if response.status_code == 200:
            items = response.json().get("items", [])
            if items:
                info = items[0].get("volumeInfo", {})
                books.append({
                    "title": info.get("title", ""),
                    "slug": slugify(info.get("title", "")),
                    "thumbnail": info.get("imageLinks", {}).get("thumbnail", ""),
                    "publishedDate": info.get("publishedDate", "Unknown"),
                    "categories": info.get("categories", ["Genel"])[0]
                })

    tmdb_token = config('TMDB_API_KEY')
    headers = {"Authorization": f"Bearer {tmdb_token}", "accept": "application/json"}
    movie_comments = Comment.objects.filter(user=user, content_type='movie').values_list('slug', flat=True).distinct()
    movies = []
    for slug in movie_comments:
        query = slug.replace('-', '+')
        url = f"https://api.themoviedb.org/3/search/movie?query={query}&language=en-US&page=1"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            results = response.json().get("results", [])
            if results:
                movie = results[0]
                movies.append({
                    "title": movie.get("title", ""),
                    "slug": slugify(movie.get("title", "")),
                    "poster_url": f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get("poster_path") else "/static/assets/images/default_movie.jpg"
                })

    series_comments = Comment.objects.filter(user=user, content_type='series').values_list('slug', flat=True).distinct()
    series = []
    for slug in series_comments:
        query = slug.replace('-', '+')
        url = f"https://api.themoviedb.org/3/search/tv?query={query}&language=en-US&page=1"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            results = response.json().get("results", [])
            if results:
                item = results[0]
                series.append({
                    "title": item.get("name", ""),
                    "slug": slugify(item.get("name", "")),
                    "poster_url": f"https://image.tmdb.org/t/p/w500{item.get('poster_path')}" if item.get("poster_path") else "/static/assets/images/default_series.jpg"
                })

    return render(request, "accounts/profile.html", {
        "userProfile": user_profile,
        "games": games,
        "books": books,
        "movies": movies,
        "series": series,
    })