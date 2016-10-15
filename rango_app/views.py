from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse('<h1>Front page</h1><a href="/rango/about">About this site</a>')


def about(request):
    return HttpResponse('<h1>About my app</h1><a href="/rango">Home</a>')
