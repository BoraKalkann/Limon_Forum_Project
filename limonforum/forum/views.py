from django.shortcuts import redirect, render
import requests
from django.http import Http404
from decouple import config
from .models import Comment
from accounts.models import UserProfile
from .forms import CommentForm
import random
import re
from django.core.paginator import Paginator
import random

def slugify(value):
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
    games_url = f"https://api.rawg.io/api/games?key={game_api_key}&page_size=6"
    response = requests.get(games_url)
    if response.status_code != 200:
        raise Http404("Oyunlar bulunamadı.")
    games = response.json().get('results', [])

    books_url = "https://www.googleapis.com/books/v1/volumes?q=subject:fiction&langRestrict=en&maxResults=20&orderBy=relevance"
    response = requests.get(books_url)
    if response.status_code != 200:
        raise Http404("Kitaplar bulunamadı.")

    data = response.json()
    items = data.get("items", [])

    if not items:
        raise Http404("Kitaplar bulunamadı.")

    books = []
    for item in items[:6]:
        info = item.get("volumeInfo", {})
        title = info.get("title", "")
        if title:  
            info["slug"] = slugify(title)
            books.append(info)

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

    movies = []
    for item in items[:6]:
        title = item.get("title", "")
        if title:
            item["slug"] = slugify(title)
            if item.get("poster_path"):
                item["poster_url"] = f"https://image.tmdb.org/t/p/w500{item['poster_path']}"
            else:
                item["poster_url"] = "" 
            movies.append(item)


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

    series = []
    for item in items[:6]:
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

def GamesCategoryPage(request):
    game_api_key = config('RAWG_API_KEY')
    query = request.GET.get("s", "").strip()
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1

    if query:
        games_url = f"https://api.rawg.io/api/games?key={game_api_key}&search={query}&page_size=40"
    else:
        games_url = f"https://api.rawg.io/api/games?key={game_api_key}&page_size=40"

    response = requests.get(games_url)

    if response.status_code != 200:
        raise Http404("Oyunlar bulunamadı.")

    all_games = response.json().get('results', [])

    paginator = Paginator(all_games, 6)

    try:
        games_page = paginator.page(page)
    except:
        raise Http404("Sayfa bulunamadı.")

    context = {
        'games_page': games_page,
        'games': all_games,
        'query': query,
    }
    return render(request, 'forum/game-category.html', context)



def BooksCategoryPage(request):
    query = request.GET.get("q", "").strip()
    page_number = int(request.GET.get("page", 1))
    max_results = 6

    search_term = query if query else "fiction"
    start_index = (page_number - 1) * max_results

    books_url = (
        f"https://www.googleapis.com/books/v1/volumes"
        f"?q={search_term}&langRestrict=en&orderBy=relevance"
        f"&startIndex={start_index}&maxResults={max_results}"
    )
    response = requests.get(books_url)
    if response.status_code != 200:
        raise Http404("Kitaplar alınamadı.")

    books = []
    data = response.json()
    items = data.get("items", [])
    for item in items:
        info = item.get("volumeInfo", {})
        title = info.get("title", "")
        image_links = info.get("imageLinks", {})
        thumbnail = image_links.get("thumbnail", "")
        if title:
            books.append({
                "title": title,
                "slug": slugify(title),
                "thumbnail": thumbnail,
                "description": info.get("description", "")[:150] + "...",
                "publishedDate": info.get("publishedDate", "Unknown"),
                "categories": info.get("categories", ["Genel"])[0]
            })

    total_books = 42  
    paginator = Paginator(range(total_books), max_results)
    page_obj = paginator.get_page(page_number)

    return render(request, "forum/book-category.html", {
        "books": books,
        "page_obj": page_obj,
        "query": query  
    })


def MoviesCategoryPage(request):
    tmdb_token = config('TMDB_API_KEY')
    headers = {
        "Authorization": f"Bearer {tmdb_token}",
        "accept": "application/json"
    }

    query = request.GET.get("q", "").strip()
    page = request.GET.get("page", 1)
    try:
        page = int(page)
    except ValueError:
        page = 1

    movies = []

    if query:
        url = f"https://api.themoviedb.org/3/search/movie?query={query}&language=en-US&page=1"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            items = data.get("results", [])
            for item in items:
                title = item.get("title", "")
                if title:
                    item["slug"] = slugify(title)
                    item["poster_url"] = f"https://image.tmdb.org/t/p/w500{item['poster_path']}" if item.get("poster_path") else "/static/assets/images/default_movie.jpg"
                    movies.append(item)
        else:
            raise Http404("Arama sonuçları alınamadı.")
    else:
        for api_page in range(1, 4):
            url = f"https://api.themoviedb.org/3/movie/popular?language=en-US&page={api_page}"
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                continue
            data = response.json()
            items = data.get("results", [])
            for item in items:
                title = item.get("title", "")
                if title:
                    item["slug"] = slugify(title)
                    item["poster_url"] = f"https://image.tmdb.org/t/p/w500{item['poster_path']}" if item.get("poster_path") else "/static/assets/images/default_movie.jpg"
                    movies.append(item)
        movies = movies[:42]

    paginator = Paginator(movies, 6)
    try:
        movies_page = paginator.page(page)
    except:
        raise Http404("Sayfa bulunamadı.")

    context = {
        "movies": movies_page,
        "movies_page": movies_page,
        "query": query,
    }
    return render(request, "forum/movie-category.html", context)


def SeriesCategoryPage(request):
    tmdb_token = config('TMDB_API_KEY')
    headers = {
        "Authorization": f"Bearer {tmdb_token}",
        "accept": "application/json"
    }

    query = request.GET.get("s", "").strip()
    try:
        page = int(request.GET.get("page", 1))
    except ValueError:
        page = 1

    series = []
    for api_page in range(1, 4):
        if query:
            url = f"https://api.themoviedb.org/3/search/tv?query={query}&language=en-US&page={api_page}"
        else:
            url = f"https://api.themoviedb.org/3/tv/popular?language=en-US&page={api_page}"

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            continue

        data = response.json()
        items = data.get("results", [])
        for item in items:
            name = item.get("name", "")
            if name:
                item["slug"] = slugify(name)
                item["poster_url"] = f"https://image.tmdb.org/t/p/w500{item['poster_path']}" if item.get("poster_path") else "/static/assets/images/default_series.jpg"
                series.append(item)

    series = series[:42]  
    paginator = Paginator(series, 6)
    try:
        series_page = paginator.page(page)
    except:
        raise Http404("Sayfa bulunamadı.")

    return render(request, "forum/series-category.html", {
        "series_page": series_page,
        "series": series,
        "query": query
    })


def contactPage(request):
    return render(request, 'forum/contact.html')

def searchResultPage(request):
    return render(request, 'forum/search-result.html')

def singleSeriesPage(request, slug):
    tmdb_token = config('TMDB_API_KEY')
    headers = {
        "Authorization": f"Bearer {tmdb_token}",
        "accept": "application/json"
    }

    search_url = f"https://api.themoviedb.org/3/search/tv?query={slug.replace('-', ' ')}&language=tr-TR"
    search_response = requests.get(search_url, headers=headers)
    if search_response.status_code != 200:
        raise Http404("Dizi bulunamadı.")
    search_results = search_response.json().get("results")
    if not search_results:
        raise Http404("Dizi bulunamadı.")

    series_data = next((s for s in search_results if slugify(s["name"]) == slug), search_results[0])
    tv_id = series_data["id"]

    detail_url = f"https://api.themoviedb.org/3/tv/{tv_id}?language=tr-TR"
    detail_response = requests.get(detail_url, headers=headers)
    if detail_response.status_code != 200:
        raise Http404("Dizi detayı alınamadı.")
    series = detail_response.json()

    popular_url = "https://api.themoviedb.org/3/tv/popular?language=tr-TR&page=1"
    popular_response = requests.get(popular_url, headers=headers)
    popular_series = popular_response.json().get("results", [])[:5] if popular_response.status_code == 200 else []

    for s in popular_series:
        poster_path = s.get("poster_path")
        s["poster_full"] = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

    comments = Comment.objects.filter(content_type='series', slug=slug, parent__isnull=True).order_by('-created_at')
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_type = 'series'
            comment.slug = slug
            comment.save()
            return redirect(request.path_info)

    return render(request, 'forum/single-series.html', {
        'series': series,
        'comments': comments,
        'form': form,
        'series_list': popular_series,
    })

def singleMoviePage(request, slug):
    tmdb_token = config('TMDB_API_KEY')
    headers = {
        "Authorization": f"Bearer {tmdb_token}",
        "accept": "application/json"
    }

    search_url = f"https://api.themoviedb.org/3/search/movie?query={slug.replace('-', ' ')}&language=tr-TR"
    search_response = requests.get(search_url, headers=headers)
    if search_response.status_code != 200:
        raise Http404("Film bulunamadı.")
    search_results = search_response.json().get("results")
    if not search_results:
        raise Http404("Film bulunamadı.")

    movie_data = next((m for m in search_results if slugify(m["title"]) == slug), search_results[0])
    movie_id = movie_data["id"]

    detail_url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=tr-TR"
    detail_response = requests.get(detail_url, headers=headers)
    if detail_response.status_code != 200:
        raise Http404("Film detayı alınamadı.")
    movie = detail_response.json()

    popular_url = "https://api.themoviedb.org/3/movie/popular?language=tr-TR&page=1"
    popular_response = requests.get(popular_url, headers=headers)
    popular_movies = popular_response.json().get("results", [])[:5] if popular_response.status_code == 200 else []

    for m in popular_movies:
        poster_path = m.get("poster_path")
        m["poster_full"] = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

    comments = Comment.objects.filter(content_type='movie', slug=slug, parent__isnull=True).order_by('-created_at')
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_type = 'movie'
            comment.slug = slug
            comment.save()
            return redirect(request.path_info)

    return render(request, 'forum/single-movie.html', {
        'movie': movie,
        'comments': comments,
        'form': form,
        'movies': popular_movies,
    })


def singleGamePage(request, slug):
    game_api_key = config('RAWG_API_KEY')
    
    game_url = f"https://api.rawg.io/api/games/{slug}?key={game_api_key}"
    response = requests.get(game_url)
    if response.status_code != 200:
        raise Http404("Game is not found.")
    game = response.json()

    popular_url = f"https://api.rawg.io/api/games?ordering=-rating&page_size=5&key={game_api_key}"
    popular_response = requests.get(popular_url)
    popular_games = popular_response.json().get("results", []) if popular_response.status_code == 200 else []

    comments = Comment.objects.filter(content_type='game', slug=slug, parent__isnull=True).order_by('-created_at')
    userProfiles = UserProfile.objects.all()
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_type = 'game'
            comment.slug = slug
            comment.save()
            return redirect(request.path_info)

    return render(request, 'forum/single-game.html', {
        'game': game,
        'comments': comments,
        'userProfiles': userProfiles,
        'form': form,
        'games': popular_games,  
    })



def singleBookPage(request, slug):
    api_url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{slug.replace('-', ' ')}&langRestrict=tr"
    response = requests.get(api_url)
    if response.status_code != 200:
        raise Http404("Kitap bulunamadı.")
    data = response.json()
    items = data.get("items")
    if not items:
        raise Http404("Kitap bulunamadı.")
    book = items[0]["volumeInfo"]

    popular_url = "https://www.googleapis.com/books/v1/volumes?q=subject:fiction&langRestrict=tr&maxResults=5"
    popular_response = requests.get(popular_url)
    popular_books = []
    if popular_response.status_code == 200:
        popular_data = popular_response.json()
        popular_items = popular_data.get("items", [])
        for item in popular_items:
            volume_info = item.get("volumeInfo", {})
            title = volume_info.get("title", "")
            slug_title = slugify(title)
            thumbnail = volume_info.get("imageLinks", {}).get("thumbnail")
            published_date = volume_info.get("publishedDate", "")
            popular_books.append({
                "title": title,
                "slug": slug_title,
                "thumbnail": thumbnail,
                "publishedDate": published_date,
            })

    comments = Comment.objects.filter(content_type='book', slug=slug, parent__isnull=True).order_by('-created_at')
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_type = 'book'
            comment.slug = slug
            comment.save()
            return redirect(request.path_info)

    return render(request, 'forum/single-book.html', {
        'book': book,
        'comments': comments,
        'form': form,
        'books': popular_books,  
    })
