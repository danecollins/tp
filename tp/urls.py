from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.contrib.auth import views as auth_views
from places import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^places/', include('places.urls', namespace="places")),
                       url(r'^blog/', include('blog.urls', namespace="blog")),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^accounts/login/$', auth_views.login),
                       url('^', include('django.contrib.auth.urls'))
                       )
