from django.shortcuts import render

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