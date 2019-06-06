from django.conf.urls import url
from vote import views
from vote.views import index

urlpatterns = [
   url(r'^$', index, name='index'),
   url(r'^man/$', views.man),
   url(r'^woman/$', views.woman),
   url(r'^survey/$', views.view_survey),
   url(r'^survey/(?P<name>[\w]+)/$', views.set_survey),
   url(r'^car/(?P<car_name>[\w]+)/$', views.add_car_vote)
]
