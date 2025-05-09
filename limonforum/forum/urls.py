from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='homePage'),
    path('about', views.aboutPage, name='aboutPage'),
    path('blog', views.blogPage, name='blogPage'),
    path('category', views.categoryPage, name='categoryPage'),
    path('contact', views.contactPage, name='contactPage'),
    path('search-result', views.searchResultPage, name='searchResultPage'),
    path('single', views.singlePage, name='singlePage'),
]
