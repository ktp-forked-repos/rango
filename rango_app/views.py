from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    context_dict = {'boldmessage': "Featured content"}
    return render(request, 'rango/index.html', context_dict)


def about(request):
    return HttpResponse('<h1>About my app</h1><a href="/rango">Home</a>')
