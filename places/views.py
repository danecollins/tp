from django.shortcuts import render
from places.models import Place
from collections import defaultdict

# Create your views here.


def index(request):
    return render(request, 'places/index.html')


def city_list(request):
    cities = sorted(set([x.city for x in Place.objects.all()]))
    return render(request, 'places/city_list.html', {'clist': cities})


def locale_list(request, city):
    places = Place.objects.filter(city=city)
    by_locale = defaultdict(set)
    for p in places:
        by_locale[p.locale].add(p.name)

    return render(request, 'places/locale_list.html', {'llist': sorted(by_locale.keys()),
                                                       'dict': by_locale,
                                                       'city': city})


def place_list(request, city, locale):
    locales = sorted(set([x.name for x in Place.objects.filter(city=city, locale=locale)]))
    return render(request, 'places/place_list.html', {'plist': locales,
                                                      'city': city,
                                                      'locale': locale})


def place_detail(request, place):
    place = Place.objects.filter(name=place)
    place = place[0]
    return render(request, 'places/place_detail.html', {'p': place})