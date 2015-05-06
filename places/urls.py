from django.conf.urls import patterns, url
from places import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^city/$', views.city_list, name='city_list'),
                       url(r'^city/(?P<city>[\w|\W]+)/$', views.locale_list, name='locale_list'),
                       url(r'^view/(?P<place_id>[\d]+)/$', views.place_detail, name='place_detail'),
                       url(r'^edit/(?P<place_id>[\d]+)/$', views.place_edit, name='place_edit'),
                       url(r'^save/(?P<place_id>[\d]+)/$', views.place_save, name='place_save'),
                       )
