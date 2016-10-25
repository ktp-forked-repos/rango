from django.shortcuts import render


def home(request):
    context_dict = {}
    return render(request, 'cms2d/index.html', context_dict)
