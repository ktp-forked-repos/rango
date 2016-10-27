from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from cms2d.forms import TopicForm
from cms2d.models import Topic


def home(request):
    context_dict = {
        'topics_by_views': Topic.objects.all()
    }

    return render(request, 'cms2d/index.html', context_dict)


@login_required
def add_topic(request, topic_name_slug=None):
    if request.method == 'POST':
        form = TopicForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return home(request)
        else:
            print form.errors

    else:
        form = TopicForm()

    return render(request, 'cms2d/add_topic.html', {'form': form})


def topic(request, topic_name_slug):
    context_dict = {}

    try:
        topic = Topic.objects.get(slug=topic_name_slug)
        context_dict['topic'] = topic
        context_dict['topic_name'] = topic.name
    except Topic.DoesNotExist:
        context_dict['topic_name'] = topic_name_slug
        pass

    return render(request, 'cms2d/topic.html', context_dict)
