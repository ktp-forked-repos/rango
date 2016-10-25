from django.conf.urls import url
from cms2d import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    #url(r'^add_category/(?P<category_name_slug>[\w\-]+)$', views.add_category, name='add_category'),
    #url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
    #url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page$', views.add_page, name='add_page'),
]
