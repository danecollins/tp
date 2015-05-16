from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.contrib.auth import views as auth_views
from config import settings

urlpatterns = patterns('',
                       url(r'^$', 'places.views.index', name='index'),
                       url(r'^places/', include('places.urls', namespace="places")),
                       url(r'^blog/', include('blog.urls', namespace="blog")),
                       url(r'^vote/', include('vote.urls', namespace="vote")),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^accounts/login/$', auth_views.login),
                       url(r'^newuser/$', 'registration.views.newuser', name='newuser'),
                       url(r'^about/$', 'places.views.about', name='about'),
                       url(r'^dane/$', 'places.views.info', name='info'),
                       url(r'^(?P<path>apple-touch-icon.png)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
                       url('^', include('django.contrib.auth.urls'))
                       )
