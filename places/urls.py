from django.conf.urls import patterns, url
from places import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^city/$', views.city_list, name='city_list'),
                       url(r'^add/$', views.place_add, name='place_add'),
                       url(r'^search/$', views.search, name='search'),
                       url(r'^city/(?P<city>[\w|\W]+)/$', views.locale_list, name='locale_list'),
                       url(r'^view/(?P<place_id>[\d]+)/$', views.place_detail, name='place_detail'),
                       url(r'^edit/(?P<place_id>[\d]+)/$', views.place_edit, name='place_edit'),
                       url(r'^save/(?P<place_id>[\d]+)/$', views.place_save, name='place_save'),
                       url(r'^share/(?P<place_id>[\d]+)/(?P<username>[\w|\W]+)/$',
                           views.place_share, name='place_share'),
                       url(r'^copy/(?P<place_id>[\d]+)/$', views.place_copy, name='place_copy'),
                       )
