from django.shortcuts import render
from places.models import Place

# Create your views here.


def index(request):
    return render(request, 'places/index.html')


def city_list(request):
    cities = sorted(set([x.city for x in Place.objects.all()]))
    return render(request, 'places/city_list.html', {'clist': cities})


def locale_list(request, city):
    locales = sorted(set([x.locale for x in Place.objects.filter(city=city)]))
    return render(request, 'places/locale_list.html', {'llist': locales,
                                                       'city': city})


def place_list(request, city, locale):
    locales = sorted(set([x.name for x in Place.objects.filter(city=city, locale=locale)]))
    return render(request, 'places/place_list.html', {'plist': locales,
                                                      'city': city,
                                                      'locale': locale})
