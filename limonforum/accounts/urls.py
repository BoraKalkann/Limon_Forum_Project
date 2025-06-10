from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'accounts'

urlpatterns = [
    path('login', views.login_view, name='loginPage'),
    path('register', views.register_view, name='registerPage'),
    path('logout', LogoutView.as_view(next_page='homePage'), name='logout'),
    path('profile', views.profile_view, name='profilePage'),
]