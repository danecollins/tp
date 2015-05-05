from django.conf.urls import patterns, include, url
from django.contrib import admin

from places import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^places/', include('places.urls',
                                                namespace="places")),
                       url(r'^admin/', include(admin.site.urls)),
                       )
