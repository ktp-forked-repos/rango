from django.conf.urls import url
from cms2d import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^add_topic$', views.add_topic, name='add_topic'),
    url(r'^topic/(?P<topic_name_slug>[\w\-]+)/$', views.topic, name='topic')
]
