from django.urls import path
from . import views


urlpatterns = [
    path('', views.homePage, name='homePage'),
    path('about', views.aboutPage, name='aboutPage'),
    path('blog', views.blogPage, name='blogPage'),
    path('category', views.categoryPage, name='categoryPage'),
    path('contact', views.contactPage, name='contactPage'),
    path('search-result', views.searchResultPage, name='searchResultPage'),
    path('single/game/<slug:slug>/', views.singleGamePage, name='singleGamePage'),
    path('single/movie/<slug:slug>/', views.singleMoviePage, name='singleMoviePage'),
    path('single/series/<slug:slug>/', views.singleSeriesPage, name='singleSeriesPage'),
    path('single/book/<slug:slug>/', views.singleBookPage, name='singleBookPage'),
    path('login/', views.login_view, name='loginPage'),
    path('register/', views.register_view, name='registerPage'),
]