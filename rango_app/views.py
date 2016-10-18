from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from rango_app.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from rango_app.models import Category, Page


# Create your views here.
def index(request):
    context_dict = {
        'categories_by_votes': Category.objects.order_by('-votes')[:5],
        'categories_by_views': Category.objects.order_by('-views')[:5]
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
    visits = request.session.get('visits') or 1
    return render(request, 'rango/about.html', {'visits': visits})


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


def register(request):
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Hash the password with the set_password method and update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # If the user provided a profile picture, get it from the input form and add it to UserProfile model
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True

        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm
        profile_form = UserProfileForm

    return render(
        request,
        'rango/register.html',
        {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}
    )


def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Get the username and password provided by the user.
        # This information is obtained from the login form.

        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        if user:
            # Check that the user account hasn't been disabled
            if user.is_active:
                # If account is valid and active, send user back to the homepage
                login(request, user)
                return HttpResponseRedirect('/rango')
            else:
                return HttpResponse("Your account has been disabled.")
        else:
            # Incorrect login details provided
            print "Invalid login details: {0} {1}".format(username, password)
            return HttpResponse("Invalid login details")
    else:
        # Not a POST requestion, so probably a GET request, so show login form
        return render(request, 'rango/login.html', {})


@login_required
def user_logout(request):
    # Since the user must be logged in, we can just log them out now
    logout(request)
    return HttpResponseRedirect('/rango')


@login_required
def restricted(request):
    return HttpResponse("You can see this page because you're logged in.")
