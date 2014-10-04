from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^authentication/', include('authentication.urls', namespace='authentication')),
    url(r'^home/', include('home.urls', namespace='home')),
    url(r'^registration/', include('registration.urls', namespace='registration')),
    url(r'^volunteer/', include('volunteer.urls', namespace="volunteer")),
)