from django.shortcuts import redirect, render
import requests
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from decouple import config

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

def singlePage(request, slug):
    
    api_key = config('RAWG_API_KEY')
    url = f"https://api.rawg.io/api/games/{slug}?key={api_key}"

    response = requests.get(url)

    if response.status_code != 200:
        raise Http404("Game is not found.")

    game = response.json()

    return render(request, 'forum/single.html', {'game': game})


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

