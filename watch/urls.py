from django.conf.urls import patterns, url
from watch import views

urlpatterns = patterns('',
                       url(r'^events/$', views.event_history),
                       url(r'^list/$', views.show),
                       url(r'^add/$', views.add),
                       url(r'^details/(?P<id>[\d]+)/$', views.details),
                       )
