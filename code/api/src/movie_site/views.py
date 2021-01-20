from django.shortcuts import render

def root(request):
    return render(request, 'movie_site/base.html')
