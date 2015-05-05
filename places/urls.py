from django.conf.urls import patterns, url
from places import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^city/$', views.city_list, name='city_list'),
                       url(r'^city/(?P<city>[\w|\W]+)/(?P<locale>[\w|\W]+)/$', views.place_list, name='place_list'),
                       url(r'^city/(?P<city>[\w|\W]+)/$', views.locale_list, name='locale_list'),
                       )
