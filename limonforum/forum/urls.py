from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='homePage'),
    path('about', views.aboutPage, name='aboutPage'),
    path('category/games', views.GamesCategoryPage, name='GamesCategoryPage'),
    path('category/books', views.BooksCategoryPage, name='BooksCategoryPage'),
    path('category/movies', views.MoviesCategoryPage, name='MoviesCategoryPage'),
    path('category/series', views.SeriesCategoryPage, name='SeriesCategoryPage'),
    path('contact', views.contactPage, name='contactPage'),
    path('search-result', views.searchResultPage, name='searchResultPage'),
    path('single/game/<slug:slug>', views.singleGamePage, name='singleGamePage'),
    path('single/movie/<slug:slug>', views.singleMoviePage, name='singleMoviePage'),
    path('single/series/<slug:slug>', views.singleSeriesPage, name='singleSeriesPage'),
    path('single/book/<slug:slug>', views.singleBookPage, name='singleBookPage'),
]