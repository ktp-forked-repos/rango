from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from rango_app.forms import CategoryForm, PageForm
from rango_app.models import Category, Page


# Create your views here.
def index(request):
    context_dict = {
        'categories_by_votes': Category.objects.order_by('-votes')[:5],
        'categories_by_views': Category.objects.order_by('-views')[:5],
        'pages_by_votes': Page.objects.order_by('-views')[:5],
    }

    visits = request.session.get('visits') or 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).days > 0:
            visits += 1
            reset_last_visit_time = True
    else:
        # Cookie doesn't exsit so we need to set it
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits

    return render(request, 'rango/index.html', context_dict)


def about(request):
    return render(request, 'rango/about.html', {})


def profile(request):
    visits = request.session.get('visits') or 1
    return render(request, 'rango/profile.html', {'visits': visits})


def category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category'] = category
        context_dict['category_name'] = category.name

        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
    except Category.DoesNotExist:
        context_dict['category_name'] = category_name_slug
        pass

    return render(request, 'rango/category.html', context_dict)


@login_required
def add_category(request, category_name_slug=None):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print form.errors

    else:
        form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form': form, 'category': cat}

    return render(request, 'rango/add_page.html', context_dict)
