from django.shortcuts import redirect, render
import requests
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from decouple import config
import pprint

def homePage(request):
    return render(request, 'forum/index.html')

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

    return render(request, 'forum/single-game.html', {'game': game})

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

