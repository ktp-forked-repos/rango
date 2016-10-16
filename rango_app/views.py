from django.shortcuts import render


# Create your views here.
def index(request):
    context_dict = {'boldmessage': "Featured content"}
    return render(request, 'rango/index.html', context_dict)


def about(request):
    return render(request, 'rango/about.html')
