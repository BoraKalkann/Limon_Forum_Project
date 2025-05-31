from django.shortcuts import redirect, render
import requests
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from decouple import config
from .models import GameComment
from .forms import GameCommentForm
import pprint
import random
import re

import random

def slugify(value):
    # Türkçe karakterleri Latin harflerine çevir
    turkish_map = str.maketrans(
        "çğıöşüÇĞİÖŞÜ",
        "cgiosuCGIOSU"
    )
    value = str(value).translate(turkish_map)
    value = value.strip().lower()
    value = re.sub(r'[^a-z0-9\s-]', '', value)
    value = re.sub(r'[\s]+', '-', value)
    return value

def homePage(request):
    game_api_key = config('RAWG_API_KEY')
    # 20 popüler oyunu çekiyoruz
    games_url = f"https://api.rawg.io/api/games?key={game_api_key}&page_size=20"
    response = requests.get(games_url)
    if response.status_code != 200:
        raise Http404("Oyunlar bulunamadı.")
    all_games = response.json().get('results', [])

    # Rastgele 6 oyun seçiyoruz
    games = random.sample(all_games, 6) if len(all_games) >= 6 else all_games

    books_url = "https://www.googleapis.com/books/v1/volumes?q=subject:fiction&langRestrict=en&maxResults=20&orderBy=relevance"
    response = requests.get(books_url)
    if response.status_code != 200:
        raise Http404("Kitaplar bulunamadı.")

    data = response.json()
    items = data.get("items", [])

    if not items:
        raise Http404("Kitaplar bulunamadı.")

    # Sadece ilk 6 kitabı alıyoruz ve slug ekliyoruz
    books = []
    for item in items[:6]:
        info = item.get("volumeInfo", {})
        title = info.get("title", "")
        if title:  # Sadece başlığı olan kitaplar
            info["slug"] = slugify(title)
            books.append(info)

    pprint.pprint(books)
    tmdb_token = config('TMDB_API_KEY')
    movies_url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
    headers = {
        "Authorization": f"Bearer {tmdb_token}",
        "accept": "application/json"
    }
    response = requests.get(movies_url, headers=headers)
    if response.status_code != 200:
        raise Http404("Filmler bulunamadı.")

    data = response.json()
    items = data.get("results", [])

    if not items:
        raise Http404("Filmler bulunamadı.")

    # Sadece ilk 9 filmi alıyoruz ve slug ekliyoruz
    movies = []
    for item in items[:9]:
        title = item.get("title", "")
        if title:
            item["slug"] = slugify(title)
            # TMDB poster_path'ı tam URL'ye çevir
            if item.get("poster_path"):
                item["poster_url"] = f"https://image.tmdb.org/t/p/w500{item['poster_path']}"
            else:
                item["poster_url"] = ""  # veya varsayılan bir görsel yolu
            movies.append(item)

    pprint.pprint(movies)

    tmdb_token = config('TMDB_API_KEY')
    series_url = "https://api.themoviedb.org/3/tv/popular?language=en-US&page=1"
    headers = {
        "Authorization": f"Bearer {tmdb_token}",
        "accept": "application/json"
    }
    response = requests.get(series_url, headers=headers)
    if response.status_code != 200:
        raise Http404("Diziler bulunamadı.")

    data = response.json()
    items = data.get("results", [])

    if not items:
        raise Http404("Diziler bulunamadı.")

    # Sadece ilk 4 diziyi alıyoruz ve slug ekliyoruz
    series = []
    for item in items[:4]:
        name = item.get("name", "")
        if name:
            item["slug"] = slugify(name)
            if item.get("poster_path"):
                item["poster_url"] = f"https://image.tmdb.org/t/p/w500{item['poster_path']}"
            else:
                item["poster_url"] = ""
            series.append(item)

    return render(request, 'forum/index.html', {'games': games, 'books': books, 'movies': movies, 'series': series})

def aboutPage(request):
    return render(request, 'forum/about.html')

def blogPage(request):
    return render(request, 'forum/blog.html')

def categoryPage(request):
    return render(request, 'forum/category.html')

def contactPage(request):
    return render(request, 'forum/contact.html')

def searchResultPage(request):
    return render(request, 'forum/search-result.html')

def singleSeriesPage(request, slug):
    
    tmdb_token = config('TMDB_API_KEY')

    search_url = f"https://api.themoviedb.org/3/search/tv?query={slug}&language=tr-TR"
    headers = {
        "Authorization": f"Bearer {tmdb_token}",
        "accept": "application/json"
    }
    search_response = requests.get(search_url, headers=headers)
    if search_response.status_code != 200:
        raise Http404("Dizi bulunamadı.")

    search_results = search_response.json().get("results")
    if not search_results:
        raise Http404("Dizi bulunamadı.")

    tv_id = search_results[0]["id"]

    detail_url = f"https://api.themoviedb.org/3/tv/{tv_id}?language=tr-TR"
    detail_response = requests.get(detail_url, headers=headers)
    if detail_response.status_code != 200:
        raise Http404("Dizi detayı alınamadı.")

    series = detail_response.json()

    return render(request, 'forum/single-series.html', {'series': series})

def singleMoviePage(request, slug):

    tmdb_token = config('TMDB_API_KEY')

    search_url = f"https://api.themoviedb.org/3/search/movie?query={slug}&language=tr-TR"
    headers = {
        "Authorization": f"Bearer {tmdb_token}",
        "accept": "application/json"
    }
    search_response = requests.get(search_url, headers=headers)
    if search_response.status_code != 200:
        raise Http404("Film bulunamadı.")

    search_results = search_response.json().get("results")
    if not search_results:
        raise Http404("Film bulunamadı.")

    movie_id = search_results[0]["id"]

    detail_url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=tr-TR"
    detail_response = requests.get(detail_url, headers=headers)
    if detail_response.status_code != 200:
        raise Http404("Film detayı alınamadı.")

    movie = detail_response.json()

    return render(request, 'forum/single-movie.html', {'movie': movie})

def singleGamePage(request, slug):
    game_api_key = config('RAWG_API_KEY')
    game_url = f"https://api.rawg.io/api/games/{slug}?key={game_api_key}"
    response = requests.get(game_url)
    if response.status_code != 200:
        raise Http404("Game is not found.")
    game = response.json()

    comments = GameComment.objects.filter(game_slug=slug, parent__isnull=True).order_by('-created_at')
    form = GameCommentForm()

    if request.method == 'POST':
        form = GameCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.game_slug = slug
            comment.save()
            return redirect('singleGamePage', slug=slug)

    return render(request, 'forum/single-game.html', {
        'game': game,
        'comments': comments,
        'form': form
    })

def singleBookPage(request, slug):

    api_url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{slug}&langRestrict=tr"

    response = requests.get(api_url)
    if response.status_code != 200:
        raise Http404("Kitap bulunamadı.")

    data = response.json()
    items = data.get("items")

    if not items:
        raise Http404("Kitap bulunamadı.")

    book = items[0]["volumeInfo"]

    return render(request, 'forum/single-book.html', {'book': book})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username = username, password = password)
    
        if user is not None:
            login(request,user)
            return redirect('homePage')
        
    return render(request, 'forum/login.html')   
 
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
        return redirect('loginPage')  
    return render(request, 'forum/register.html')

