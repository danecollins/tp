from django.conf.urls import patterns, url
from vote import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^man/$', views.man, name='man'),
                       url(r'^woman/$', views.woman, name='man'),
                       )
