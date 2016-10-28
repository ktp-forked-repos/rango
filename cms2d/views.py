from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from cms2d.forms import TopicForm
from cms2d.models import Topic, User


def home(request):
    context_dict = {
        'topics_by_views': Topic.objects.all()
    }

    return render(request, 'cms2d/index.html', context_dict)


@login_required
def add_topic(request, topic_name_slug=None):
    if request.method == 'POST':
        #form = TopicForm(request.POST, initial={"author_id": request.user.id})
        form = TopicForm(request.POST)

        if form.is_valid():
            model = form.save(commit=True)
            return redirect('topic', topic_name_slug=model.slug)
        else:
            print form.errors

    else:
        form = TopicForm(initial={"author_id": request.user.id})

    return render(request, 'cms2d/add_topic.html', {'form': form})


def topic(request, topic_name_slug):
    context_dict = {}

    try:
        topic = Topic.objects.get(slug=topic_name_slug)

        try:
            author = User.objects.get(pk=topic.author_id)
            context_dict['author'] = author
        except User.DoesNotExist:
            pass

        context_dict['topic'] = topic
        context_dict['topic_name'] = topic.name
    except Topic.DoesNotExist:
        context_dict['topic_name'] = topic_name_slug
        pass

    return render(request, 'cms2d/topic.html', context_dict)
