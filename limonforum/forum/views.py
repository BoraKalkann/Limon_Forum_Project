from django.shortcuts import render

def homePage(request):
    return render(request, 'index.html')

def aboutPage(request):
    return render(request, 'about.html')

def blogPage(request):
    return render(request, 'blog.html')

def categoryPage(request):
    return render(request, 'category.html')

def contactPage(request):
    return render(request, 'contact.html')

def searchResultPage(request):
    return render(request, 'search-result.html')

def singlePage(request):
    return render(request, 'single.html')