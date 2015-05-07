from django.conf.urls import patterns, url
from blog import views

urlpatterns = patterns('',
    url(r'^post/(?P<slug>[-\w]+)$', views.view_post, name='detail'),
    url(r'^add/$', views.add_post, name='add_post'),
    url(r'^archive$', views.archive, name='archive')
)
