from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import requests
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

    if request.method == "POST":
        user = request.user
        name = request.POST.get("name", "").strip()
        surname = request.POST.get("surname", "").strip()
        bio = request.POST.get("bio", "").strip()
        image = request.FILES.get("image")

        user.first_name = name
        user.last_name = surname
        user_profile, created = UserProfile.objects.get_or_create(user = user)

        if bio:
            user_profile.bio = bio
        if image:
            user_profile.image = image
        
        user_profile.save()
        user.save()

        return redirect("accounts:profilePage")
    
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    comments = Comment.objects.filter(user=request.user).values('content_type', 'slug').distinct()

    game_api_key = config('RAWG_API_KEY')
    games = []
    for item in comments:
        if item['content_type'] == 'game':
            slug = item['slug']
            game_url = f"https://api.rawg.io/api/games/{slug}?key={game_api_key}"
            response = requests.get(game_url)
            if response.status_code == 200:
                games.append(response.json())
    
    data = {
        "userProfile": user_profile,
        "commented_games": games,
    }

    return render(request, 'accounts/profile.html', data)


