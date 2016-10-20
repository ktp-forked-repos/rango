"""Rango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from registration.backends.simple.views import RegistrationView

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib import admin


# Class that redirects the user to the index page after successfully logging in
class MyRegistrationView(RegistrationView):
    def get_success_url(self, request, user):
        return '/rango/'


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'rango/', include('rango_app.urls')),
    url(r'^accounts/register$', MyRegistrationView.as_view(), name="registration_register"),
    url(r'^accounts/', include('registration.backends.simple.urls'))
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT
            }
        )
        #static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        #url(r'^media/(?P<path>.*)', 'django.views.static.serve')
    ]
