from django.conf.urls import patterns, url
from watch import views

urlpatterns = patterns('',
                       url(r'^events/$', views.event_history),
                       url(r'^checkin/(?P<tag>.*)/$', views.checkin),
                       url(r'^list/$', views.list),
                       url(r'^add/$', views.add),
                       url(r'^details/(?P<id>[\d]+)/$', views.detail),
                       url(r'^edit/(?P<id>[\d]+)/$', views.edit),
                       )
