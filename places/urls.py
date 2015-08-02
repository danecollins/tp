from django.conf.urls import patterns, url
from places import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^(?P<pltype>[\w]+)/city/$', views.city_list, name='city_list'),
                       url(r'^(?P<pltype>[\w]+)/add/$', views.place_add, name='place_add'),
                       url(r'^(?P<pltype>[\w]+)/search/$', views.search),
                       url(r'^(?P<pltype>[\w]+)/city/(?P<city>[\w|\W]+)/$', views.locale_list),

                       url(r'^visits/$', views.visit_list),
                       url(r'^view/(?P<place_id>[\d]+)/$', views.place_detail, name='place_detail'),
                       url(r'^edit/(?P<place_id>[\d]+)/$', views.place_edit, name='place_edit'),
                       url(r'^save/(?P<place_id>[\d]+)/$', views.place_save, name='place_save'),
                       url(r'^share/(?P<place_id>[\d]+)/$', views.place_share, name='place_share'),
                       url(r'^copy/(?P<place_id>[\d]+)/$', views.place_copy, name='place_copy'),
                       url(r'^delete/(?P<place_id>[\d]+)/$', views.delete),
                       url(r'^visit/(?P<place_id>[\d]+)/$', views.visit),
                       )
