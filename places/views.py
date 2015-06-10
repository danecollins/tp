from __future__ import print_function
from django.shortcuts import render, get_object_or_404

from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django.contrib.auth.models import User
from .models import Place, VisitType, Visit
from .forms import PlaceForm
from vote.models import Vote, Survey

import re
import sys
import os
import pdb

opentable_data = {}
opentable_data[9] = (2493, 'capers-reservations-campbell', 'Capers (2493)')
opentable_data[44] = (2550, 'forbes-mill-steakhouse-los-gatos-reservations-los-gatos',
                      "Forbes Mill Steakhouse - Los Gatos (2550)")
opentable_data[46] = (61927, 'rosie-mccanns-irish-pub-and-restaurant-reservations-santa-cruz',
                      "Rosie McCann's - Santa Cruz (61927)")
opentable_data[119] = (3961, 'frasca-food-and-wine-reservations-boulder', 'Frasca Food and Wine (3961)')
opentable_data[23] = (38101, "gabriella-cafe-reservations-santa-cruz", "Gabriella Cafe (38101)")
opentable_data[10] = (148627, "i-gatti-reservations-los-gatos", "I Gatti (148627)")
opentable_data[125] = (23185, "jax-fish-house-reservations-boulder", "Jax Fish House - Boulder (23185)")
opentable_data[51] = (50125, "johnnys-harborside-reservations-santa-cruz", "Johnny's Harborside (50125)")
opentable_data[22] = (169, "kuletos-reservations-san-francisco", "Kuleto's (169)")
opentable_data[17] = (36079, "kyoto-palace-restaurant-reservations-campbell", "Kyoto Palace Restaurant (36079)")
opentable_data[27] = (7055, "lb-steak-santana-row-reservations-san-jose", "LB Steak - Santana Row (7055)")
opentable_data[14] = (60544, "laili-reservations-santa-cruz", "Laili (60544)")
opentable_data[19] = (1131, "los-gatos-brewing-company-reservations-los-gatos", "Los Gatos Brewing Company (1131)")
opentable_data[20] = (15076, "maggianos-reservations-san-jose", "Maggiano's - San Jose (183) (15076)")
opentable_data[16] = (44584, "oswald-reservations-santa-cruz", "Oswald (44584)")
opentable_data[21] = (10363, "wine-cellar-restaurant-reservations-los-gatos", "Wine Cellar Restaurant (10363)")
opentable_data[46] = (61927, "rosie-mccanns-irish-pub-and-restaurant-reservations-santa-cruz", "Rosie McCann's Irish Pub (61927)")
opentable_data[136] = (2875, "shadowbrook-restaurant-reservations-capitola", "Shadowbrook Restaurant Capitola (2875)")
opentable_data[38] = (3130, "village-california-bistro-and-wine-bar-reservations-san-jose", "Village California Bistro (3130)")
opentable_data[140] = (52660, "le-garage-reservations-sausalito", "Le Garage (52660)")
opentable_data[174] = (114103, "hults-reservations-los-gatos", "Hult's (114103)")
opentable_data[186] = (91789, 'dry-creek-grill-reservations-san-jose', "Dry Creek Grill (91789)")



def get_opentable(id):
    id = int(id)
    if id not in opentable_data:
        return False

    (restid, link, name) = opentable_data[id]
    s = '<script type="text/javascript" \
src="https://secure.opentable.com/frontdoor/default.aspx?rid={0}&restref={0}&\
bgcolor=FFFFFF&titlecolor=0F0F0F&subtitlecolor=0F0F0F&\
btnbgimage=https://secure.opentable.com/frontdoor/img/ot_btn_red.png&\
otlink=FFFFFF&icon=dark&mode=short&hover=1">\
</script>'.format(restid)
    href = '<a href="http://www.opentable.com/{1}?rtype=ism&restref={0}" class="OT_ExtLink">{2}</a>'.format(restid, link, name)
    return s + href


def log_to_slack(message):
    slack_token = os.environ.get('SLACK_TP', False)
    tp_server = os.environ.get('TP_SERVER', False)
    if slack_token:
        import requests
        import json

        url = 'https://hooks.slack.com/services/{}'.format(slack_token)
        bot_name = tp_server or 'heroku_p'
        payload = {'text': message, 'username': bot_name, }
        requests.post(url, data=json.dumps(payload))


def logprint(s):
    s = 'app_log: ' + s
    if os.environ.get('DB', False):
        print(s)
    else:
        print(s, file=sys.stderr)


def index(request):
    logprint('User: {} is on home page'.format(request.user))
    if request.user.username == 'admin':
        logout(request)
    return render(request, 'places/index.html', {'last': Place.last_added()})


def city_list(request):
    if request.user.is_anonymous():
        username = 'Guest User'
        cities = sorted(set([x.city for x in Place.objects.filter(archived=False)]))
    else:
        username = request.user.first_name
        cities = sorted(set([x.city for x in Place.objects.filter(user=request.user, archived=False)]))

    logprint('User: {} is on city list'.format(request.user))
    return render(request, 'places/city_list.html', {'clist': cities,
                                                     'username': username})


def info(request):
    data = {}
    data['username'] = "{}".format(request.user)
    data['num_users'] = len(User.objects.all())
    data['num_places'] = len(Place.objects.all())
    data['men_votes'] = len(Vote.objects.filter(type=False))
    data['women_votes'] = len(Vote.objects.filter(type=True))
    data['survey'] = Survey.get()
    data['visits'] = len(Visit.objects.all())

    # get server information
    s = os.environ.get('TP_SERVER', 'Missing')
    x = os.environ.get('DATABASE_URL', '/Missing')
    d = x.split('/')[-1]
    debug = os.environ.get('DJANGO_DEBUG', 'Missing')
    logprint('User: {} is on info page'.format(request.user))
    return render(request, 'places/info.html',
                  {'data': data, 'server': s, 'database': d, 'debug': debug})


def locale_list(request, city):
    unset = u'\u2753'
    checked = u'\u2705'
    unchecked = u'\u274C'

    if request.method == 'GET':
        args = {'outdoor': unset, 'dog_friendly': unset, 'cuisine': ''}
    else:
        print('Setting args to post method', file=sys.stderr)
        args = request.POST

    logprint('User:{} is on search page'.format(request.user))

    if request.user.is_anonymous():
        username = 'Guest User'
        places = []
        # we can end up with duplicate places due to multiple users which we don't want
        place_names = set()
        for place in Place.objects.filter(city=city, archived=False):
            if place.name not in place_names:
                place_names.add(place.name)
                places.append(place)
    else:
        username = request.user.username
        places = Place.objects.filter(city=city, user=request.user, archived=False)

    if 'cuisine' in args and args['cuisine'] != '':
        print('Filtering by cuisine={}'.format(args['cuisine']), file=sys.stderr)
        places = [x for x in places if x.cuisine == args['cuisine']]
    else:
        print('No cuisine filtering')

    if 'outdoor' in args and args['outdoor'] != unset:
        if args['outdoor'] == unchecked:
            value = False
        else:
            value = True
        print('Filtering by outdoor={}'.format(value), file=sys.stderr)
        places = [x for x in places if x.outdoor == value]

    if 'dog_friendly' in args and args['dog_friendly'] != unset:
        if args['dog_friendly'] == unchecked:
            value = False
        else:
            value = True
        print('Filtering by dog_friendly={}'.format(value), file=sys.stderr)
        places = [x for x in places if x.dog_friendly == value]

    by_locale = defaultdict(set)
    id_by_name = {p.name: p.id for p in places}
    for p in places:
        by_locale[p.locale].add(p.name)

    cuisine_list = set([x.cuisine for x in places])
    cuisine_list = sorted(cuisine_list)
    return render(request, 'places/locale_list.html', {'llist': sorted(by_locale.keys()),
                                                       'dict': by_locale,
                                                       'ids': id_by_name,
                                                       'city': city,
                                                       'username': username,
                                                       'cuisine_list': cuisine_list,
                                                       'args': args})


# we don't need to check the user since the place is found by id
def place_detail(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    if request.user.is_anonymous() or request.user != place.user:
        anon = True
        last = ''
    else:
        anon = False
        last = Visit.last_visit(place, request.user)
        if last is None:
            last = 'None Stored'
        else:
            last = str(last.when)

    logprint('User: {} is viewing details on {}'.format(request.user, place.name))
    return render(request, 'places/place_detail.html',
                  {'p': place, 'visittype': VisitType.as_string(place.visited),
                   'last': last, 'anon': anon, 'opentable': get_opentable(place_id)})


@login_required
def visit(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    user = request.user

    visit, created = Visit.objects.get_or_create(place=place, user=user)
    if created:
        logprint('User: {} added a visit to {}'.format(user, place.name))
    return place_detail(request, place_id)


@login_required
def place_edit(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    init = {'name': place.name,
            'city': place.city,
            'locale': place.locale,
            'cuisine': place.cuisine,
            'outdoor': place.outdoor,
            'dog_friendly': place.dog_friendly,
            'visited': place.visited,
            'rating': place.rating,
            'good_for': place.good_for,
            'comment': place.comment,
            'yelp': place.yelp}
    logprint('User: {} is editing place: {}'.format(request.user, place.name))
    if request.user == place.user:
        form = PlaceForm(initial=init)
        return render(request, 'places/place_edit.html',
                      {'p': place, 'form': form})
    else:
        return render(request, 'places/no_permission.html', {'p': place})


@login_required
def place_add(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PlaceForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            d = form.cleaned_data
            p = Place(user=request.user,
                      name=d['name'].strip(),
                      city=d['city'].strip(),
                      locale=d['locale'].strip(),
                      visited=d['visited'],
                      rating=d['rating'])
            p.id = Place.next_id()
            p.cuisine = d['cuisine']
            p.good_for = d['good_for']
            p.comment = d['comment']
            p.yelp = d['yelp']
            p.dog_friendly = d['dog_friendly']
            p.outdoor = d['outdoor']
            p.save()
            m = 'User: {} added place: {} with id: {}'.format(p.user, p.name, p.id)
            logprint(m)
            # log_to_slack(m)
            return place_detail(request, p.id)
    else:
        form = PlaceForm().as_table()
    return render(request, 'places/place_add.html', {'form': form})


@login_required
def place_share(request, place_id, username):
    pass
    return place_detail(request, place_id)


@login_required
def place_copy(request, place_id):
    source = get_object_or_404(Place, id=place_id)

    place = Place(user=request.user,
                  name=source.name,
                  city=source.city,
                  locale=source.locale,
                  cuisine=source.cuisine,
                  dog_friendly=source.dog_friendly,
                  outdoor=source.outdoor,
                  yelp=source.yelp,
                  )

    place.id = Place.next_id()
    place.save()
    m = 'User: {} copied place: {}'.format(request.user, place.name)
    logprint(m)
    log_to_slack(m)
    return place_edit(request, place.id)


@login_required
def place_save(request, place_id):
    args = request.POST
    p = get_object_or_404(Place, id=place_id)
    # this is not necessary but I only want to change the fields that have changed
    # rather than overwriting all of them.  I'm hoping this is visible in the logs.
    changed = []
    for k, v in args.items():
        if k == 'comment':
            if p.comment != v:
                p.comment = v
                changed.append('comment')
        elif k == 'good_for':
            if p.good_for != v:
                p.good_for = v
                changed.append('good_for')
        elif k == 'dog_friendly':
            bool_val = (v == 'on')
            if p.dog_friendly != bool_val:
                p.dog_friendly = bool_val
                changed.append('dog_friendly')
        elif k == 'outdoor':
            bool_val = (v == 'on')
            if p.outdoor != bool_val:
                p.outdoor = bool_val
                changed.append('outdoor')
        elif k == 'city':
            if p.city != v:
                p.city = v.strip()
                changed.append('city')
        elif k == 'cuisine':
            if p.cuisine != v:
                p.cuisine = v
                changed.append('cuisine')
        elif k == 'yelp':
            if p.yelp != v:
                p.yelp = v
                changed.append('yelp')
        elif k == 'locale':
            if p.locale != v:
                p.locale = v.strip()
                changed.append('locale')
        elif k == 'name':
            if p.name != v:
                p.name = v.strip()
                changed.append('name')
        elif k == 'rating':
            try:
                int_val = int(v)
            except ValueError:
                int_val = 0
            if p.rating != int_val:
                p.rating = int_val
                changed.append('rating')
        elif k == 'visited':
            int_val = int(v)
            if p.visited != int_val:
                p.visited = int_val
                changed.append('visited')

    # need to handle the checkboxes
    if p.outdoor:
        if 'outdoor' not in args:
            p.outdoor = False
            changed.append('outdoor')

    if p.dog_friendly:
        if 'dog_friendly' not in args:
            p.dog_friendly = False
            changed.append('dog_friendly')

    if changed is not None:
        logprint('User: {} edited place: {}. Changed fields: {}'.format(request.user, p.name,
                                                                        ','.join(changed)))
        p.save()
    return render(request, 'places/place_detail.html',
                  {'p': p, 'visittype': VisitType.as_string(p.visited)})


def search(request):
    if request.method == 'GET':
        places = Place.objects.filter(archived=False)
        args = {}
        logprint('User:{} is on search page'.format(request.user, args.get('pat', '')))
    else:
        args = request.POST
        pat = re.compile(args['pat'], re.IGNORECASE)
        places = [p for p in Place.objects.filter(archived=False)
                  if pat.search(p.name) or pat.search(p.cuisine) or pat.search(p.city)]
        logprint('User:{} searched for: {}'.format(request.user, args.get('pat', '')))

    # create a unique set of places, want to prefer places you own
    # create a dict based on place names
    p_by_name = defaultdict(list)
    for p in places:
        p_by_name[p.name].append(p)

    # if there are multiple places with same name, keep the one the user owns
    for k, v in p_by_name.items():
        if len(v) > 1:
            tmp = [x for x in v if x.user == request.user]
            if len(tmp) == 0:  # user owns none, keep first one
                p_by_name[k] = v[:1]
            elif len(tmp) == 1:  # user owns one, keep that one
                p_by_name[k] = tmp
            else:  # user owns multiple, keep just one
                p_by_name[k] = tmp[:1]

    # now all p_by_name have just one item
    places = [x[0] for x in p_by_name.values()]
    places = sorted(places, key=lambda p: p.name)

    return render(request, 'places/search.html',
                  {'places': places, 'args': args})


def delete(request, place_id):
    p = Place.objects.get(id=place_id)
    if request.method == 'GET':
        return render(request, 'places/confirm.html', {'place': p})
    else:
        args = request.POST
        answer = args['confirm']

        if answer == 'Yes':
            p.archived = True
            p.save()
            logprint('User: {} deleted place named: {}'.format(request.user, p.name))
            return city_list(request)
        else:
            return place_detail(request, p.id)


def about(request):
    logprint('User:{} is on about page'.format(request.user))
    return render(request, 'places/about.html')
