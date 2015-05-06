from django.shortcuts import render
from places.models import Place
from collections import defaultdict
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    return render(request, 'places/index.html')


@login_required
def city_list(request):
    cities = sorted(set([x.city for x in Place.objects.all()]))
    return render(request, 'places/city_list.html', {'clist': cities})


@login_required
def locale_list(request, city):
    places = Place.objects.filter(city=city)
    by_locale = defaultdict(set)
    id_by_name = {p.name: p.id for p in places}
    for p in places:
        by_locale[p.locale].add(p.name)

    return render(request, 'places/locale_list.html', {'llist': sorted(by_locale.keys()),
                                                       'dict': by_locale,
                                                       'ids': id_by_name,
                                                       'city': city})


# def place_list(request, city, locale):
#     locales = sorted(set([x.name for x in Place.objects.filter(city=city, locale=locale)]))
#     return render(request, 'places/place_list.html', {'plist': locales,
#                                                       'city': city,
#                                                       'locale': locale})


@login_required
def place_detail(request, place_id):
    place = Place.objects.filter(id=place_id)
    place = place[0]
    return render(request, 'places/place_detail.html', {'p': place})


@login_required
def place_edit(request, place_id):
    place = Place.objects.get(id=place_id)

    return render(request, 'places/place_edit.html', {'p': place})


@login_required
def place_save(request, place_id):
    args = request.POST
    p = Place.objects.get(id=place_id)
    changed = False
    for k, v in args.items():
        if k == 'comment':
            if p.comment != v:
                p.comment = v
                changed = True
        elif k == 'good_for':
            if p.good_for != v:
                p.good_for = v
                changed = True
        elif k == 'dog_friendly':
            bool_val = (v == 'on')
            if p.dog_friendly != bool_val:
                p.dog_friendly = bool_val
                changed = True
        elif k == 'outdoor':
            bool_val = (v == 'on')
            if p.outdoor != bool_val:
                p.outdoor = bool_val
                changed = True
        elif k == 'city':
            if p.city != v:
                p.city = v
                changed = True
        elif k == 'yelp':
            if p.yelp != v:
                p.yelp = v
                changed = True
        elif k == 'locale':
            if p.locale != v:
                p.locale = v
                changed = True
        elif k == 'rating':
            int_val = int(v)
            if p.rating != int_val:
                p.rating = int_val
                changed = True
    if changed:
        p.save()
    return render(request, 'places/place_detail.html', {'p': p})
