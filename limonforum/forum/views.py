from django.shortcuts import render
import requests
from django.http import JsonResponse

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

def singlePage(request):
    return render(request, 'forum/single.html')
def login_view(request):
    return render(request, 'forum/login.html')    
def register_view(request):
    return render(request, 'forum/register.html')
# views.py
import requests
from django.http import JsonResponse

def games_proxy(request):
    response = requests.get("https://www.freetogame.com/api/games")
    data = response.json()
    return JsonResponse(data, safe=False)
