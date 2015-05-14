from __future__ import print_function
from django.shortcuts import render
from places.models import Place
from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
import re
import pdb
import sys


def index(request):
    print('Home Page Request: User is {}'.format(request.user))
    if request.user.username == 'admin':
        logout(request)
    return render(request, 'places/index.html')


def city_list(request):
    if request.user.is_anonymous():
        username = 'Guest User'
        cities = sorted(set([x.city for x in Place.objects.all()]))
    else:
        username = request.user.first_name
        cities = sorted(set([x.city for x in Place.objects.filter(user=request.user)]))

    return render(request, 'places/city_list.html', {'clist': cities,
                                                     'username': username})


def locale_list(request, city):
    if request.user.is_anonymous():
        username = 'Guest User'
        places = []
        # we can end up with duplicate places due to multiple users which we don't want
        place_names = set()
        for place in Place.objects.filter(city=city):
            if place.name not in place_names:
                place_names.add(place.name)
                places.append(place)
    else:
        username = request.user.username
        places = Place.objects.filter(city=city, user=request.user)

    by_locale = defaultdict(set)
    id_by_name = {p.name: p.id for p in places}
    for p in places:
        by_locale[p.locale].add(p.name)

    return render(request, 'places/locale_list.html', {'llist': sorted(by_locale.keys()),
                                                       'dict': by_locale,
                                                       'ids': id_by_name,
                                                       'city': city,
                                                       'username': username})


# def place_list(request, city, locale):
#     locales = sorted(set([x.name for x in Place.objects.filter(city=city, locale=locale)]))
#     return render(request, 'places/place_list.html', {'plist': locales,
#                                                       'city': city,
#                                                       'locale': locale})

# we don't need to check the user since the place is found by id
def place_detail(request, place_id):
    place = Place.objects.get(id=place_id)
    return render(request, 'places/place_detail.html', {'p': place,
                                                        'anon': request.user.is_anonymous()})


@login_required
def place_edit(request, place_id):
    place = Place.objects.get(id=place_id)
    return render(request, 'places/place_edit.html', {'p': place})


@login_required
def place_add(request):
    if request.method == 'GET':
        return render(request, 'places/place_add.html')
    else:
        args = request.POST

        p = Place()
        p.id = None
        p.name = args['name']
        p.city = args['city']
        p.locale = args['locale']
        p.cuisine = args['cuisine']
        p.rating = int(args['rating'])
        p.good_for = args['good_for']
        p.comment = args['comment']
        p.yelp = args['yelp']
        p.dog_friendly = 'dog_friendly' in args
        p.outdoor = 'ourdoor' in args
        p.user = request.user
        p.save()
        print('User:{} added Place:{}'.format(request.user, p.name))
        return place_detail(request, p.id)


@login_required
def place_share(request, place_id, username):
    place = Place.objects.get(id=place_id)
    user = User.objects.get(username=username)
    place.id = None
    place.user = user
    place.save()
    return place_detail(request, place_id)


@login_required
def place_copy(request, place_id):
    source = Place.objects.get(id=place_id)

    place = Place(user=request.user,
                  name=source.name,
                  city=source.city,
                  locale=source.locale,
                  cuisine=source.cuisine,
                  dog_friendly=source.dog_friendly,
                  outdoor=source.outdoor,
                  yelp=source.yelp,
                  )
    place.id = None
    place.save()
    return place_edit(request, place.id)


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
        elif k == 'cuisine':
            if p.cuisine != v:
                p.cuisine = v
                changed = True
        elif k == 'yelp':
            if p.yelp != v:
                p.yelp = v
                changed = True
        elif k == 'locale':
            if p.locale != v:
                p.locale = v
                changed = True
        elif k == 'name':
            if p.name != v:
                p.name = v
                changed = True
        elif k == 'rating':
            int_val = int(v)
            if p.rating != int_val:
                p.rating = int_val
                changed = True
    if changed:
        p.save()
    return render(request, 'places/place_detail.html', {'p': p})


def search(request):
    if request.method == 'GET':
        places = Place.objects.all()
        args = {}
    else:
        args = request.POST
        pat = re.compile(args['pat'], re.IGNORECASE)
        places = [p for p in Place.objects.all() if pat.search(p.name)]

    places = sorted(places, key=lambda p: p.name)
    print('User:{} searched for:{}'.format(request.user, args.get('pat', '')))
    return render(request, 'places/search.html',
                  {'places': places, 'args': args})


def about(request):
    print('User:{} looked at about page'.format(request.user))
    return render(request, 'places/about.html')
