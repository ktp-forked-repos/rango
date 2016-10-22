from django.conf.urls import url
from rango_app import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about$', views.about, name='about'),
    url(r'^profile$', views.profile, name='profile'),
    url(r'^add_category$', views.add_category, name='add_category'),
    url(r'^add_category/(?P<category_name_slug>[\w\-]+)$', views.add_category, name='add_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page$', views.add_page, name='add_page'),
    url(r'^like_category/$', views.like_category, name='like_category'),
    url(r'^goto$', views.track_url, name='goto')
]
