from django.conf.urls import include, url
from django.contrib import admin

from django.contrib.auth import views as auth_views
import django.views.static
from config import settings

import places.views
import registration.views


urlpatterns = [
    url(r'^$', places.views.index, name='index'),
    url(r'^places/', include('places.urls', namespace="places")),
    url(r'^blog/', include('blog.urls', namespace="blog")),
    url(r'^vote/', include('vote.urls', namespace="vote")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^newuser/$', registration.views.newuser, name='newuser'),
    url(r'^about/$', places.views.about, name='about'),
    url(r'^dane/$', places.views.info, name='info'),
    url(r'^(?P<path>apple-touch-icon.png)$', django.views.static.serve, {'document_root': settings.STATIC_ROOT}),
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout')
]
