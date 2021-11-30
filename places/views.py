from __future__ import print_function
from django.shortcuts import render, get_object_or_404, redirect

from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

import twilio
from twilio.rest import TwilioRestClient
import re
import sys
import os

from django.contrib.auth.models import User
from places.models import Place, VisitType, Visit, ChangeLog
from places.forms import ShareForm, RestaurantForm, HotelForm
from vote.models import Vote, Survey
from places.yelp import get_yelp_matches, get_yelp_business


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
opentable_data[46] = (61927, "rosie-mccanns-irish-pub-and-restaurant-reservations-santa-cruz",
                      "Rosie McCann's Irish Pub (61927)")
opentable_data[136] = (2875, "shadowbrook-restaurant-reservations-capitola",
                       "Shadowbrook Restaurant Capitola (2875)")
opentable_data[38] = (3130, "village-california-bistro-and-wine-bar-reservations-san-jose",
                      "Village California Bistro (3130)")
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
    href = '<a href="http://www.opentable.com/{1}?rtype=ism&restref={0}" class="OT_ExtLink">{2}</a>'.format(restid, link, name)  # noqa
    return s + href


def pltype_url_string(p):
    if p.pltype == Place.RESTAURANT:
        return 'rest'
    else:
        return 'hotel'


def pltype_user_string(p):
    if p.pltype == Place.RESTAURANT:
        return 'Restaurant'
    else:
        return 'Hotel'


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


def city_list(request, pltype='rest'):
    if pltype == 'rest':
        query = Place.restaurants.all()
    else:
        query = Place.hotels.all()

    if request.user.is_anonymous():
        username = 'Guest User'
        cities = sorted(set([x.city for x in query.all()]))
    else:
        username = request.user.first_name
        cities = sorted(set([x.city for x in query.filter(user=request.user)]))

    place_count = Place.objects.all().count()

    # ChangeLog.view_city_list(username=request.user.username)
    logprint('User: {} is on city list'.format(request.user))
    return render(request, 'places/city_list.html', {'clist': cities,
                                                     'pltype': pltype,
                                                     'pcnt': place_count,
                                                     'username': username})


def info(request):
    data = {}
    data['username'] = "{}".format(request.user)
    data['num_users'] = len(User.objects.all())
    data['num_places'] = len(Place.objects.all())
    data['men_votes'] = len(Vote.objects.filter(survey=Survey.get(), type=False))
    data['women_votes'] = len(Vote.objects.filter(survey=Survey.get(), type=True))
    data['survey'] = Survey.get()
    data['visits'] = len(Visit.objects.all())
    data['events'] = len(ChangeLog.objects.all())

    # get server information
    s = os.environ.get('TP_SERVER', 'Missing')
    x = os.environ.get('DATABASE_URL', '/Missing')
    d = x.split('/')[-1]
    debug = os.environ.get('DJANGO_DEBUG', 'Missing')
    yelp_errs = Place.objects.filter(archived=False, yelp='')
    last_events = ChangeLog.objects.all().order_by('-id')[:20]
    logprint('User: {} is on info page'.format(request.user))
    return render(request, 'places/info.html',
                  {'data': data, 'server': s, 'database': d,
                   'debug': debug, 'yelp_errs': yelp_errs,
                   'events': last_events})


def locale_list(request, city, pltype='rest'):

    if request.method == 'GET':
        args = {'outdoor': False, 'dog_friendly': False, 'has_bar': False, 'cuisine': ''}
    else:
        print('Setting args to post method', file=sys.stderr)
        args = request.POST

    ChangeLog.view_locale_list(username=request.user.username)
    logprint('User:{} is on search page'.format(request.user))

    if request.user.is_anonymous():
        username = 'Guest User'
        places = []
        # we can end up with duplicate places due to multiple users which we don't want
        place_names = set()
        if pltype == 'rest':
            query = Place.restaurants.all()
        else:
            query = Place.hotels.all()
        for place in query.filter(city=city):
            if place.name not in place_names:
                place_names.add(place.name)
                places.append(place)
    else:
        # get places for specific user
        username = request.user.username
        if pltype == 'rest':
            places = Place.restaurants.filter(city=city, user=request.user)
        else:
            places = Place.hotels.filter(city=city, user=request.user)

    # execute filters on the page
    if 'cuisine' in args and args['cuisine'] != '':
        # print('Filtering by cuisine={}'.format(args['cuisine']), file=sys.stderr)
        places = [x for x in places if x.cuisine == args['cuisine']]
    else:
        print('No cuisine filtering')

    if 'outdoor' in args and args['outdoor']:
        # print('Filtering by outdoor', file=sys.stderr)
        places = [x for x in places if x.outdoor]

    if 'has_bar' in args and args['has_bar']:
        # print('Filtering by outdoor', file=sys.stderr)
        places = [x for x in places if x.has_bar]

    if 'dog_friendly' in args and args['dog_friendly']:
        print('Filtering by dog_friendly', file=sys.stderr)
        places = [x for x in places if x.dog_friendly]

    # we want to group by locale and for each locale sort by name
    # since you can't access items in a dict in a templace we have to 
    # create this odd data structure
    sorted_locales = sorted(set([p.locale for p in places]))
    locale_list = []
    for locale in sorted_locales:
        places_in_locale = sorted([p for p in places if p.locale == locale], key=lambda x: x.name)
        locale_list.append([locale, [(p.name, p.comment, p.good_for, p.id) for p in places_in_locale]])

    cuisine_list = sorted(set([x.cuisine for x in places]))
    for locale, places in locale_list:
        print(locale)
        for p in places:
            print(p[0], p[1], p[2])

    return render(request, 'places/locale_list.html', {'locale_list': locale_list,
                                                       'city': city,
                                                       'username': username,
                                                       'cuisine_list': cuisine_list,
                                                       'pltype': pltype,
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

    if not anon:
        ChangeLog.place_detail(place, request.user.username)
    logprint('User: {} is viewing details on {}'.format(request.user, place.name))
    return render(request, 'places/place_detail.html',
                  {'p': place, 'visittype': VisitType.as_string(place.visited),
                   'pltype': pltype_url_string(place), 'pltypeS': pltype_user_string(place),
                   'last': last, 'anon': anon, 'opentable': get_opentable(place_id)})


@login_required
def visit(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    user = request.user

    # need to select when the visit was
    if request.method == 'POST':
        form = request.POST
        visit_date = form['visit_date']
        visit, created = Visit.objects.get_or_create(place=place, user=user, when=visit_date)
        visit.save()
        if created:
            logprint('User: {} added a visit to {}'.format(user, place.name))
        return place_detail(request, place_id)
    else:
        return render(request, 'places/visit_form.html', {'place': place})


@login_required
def visit_list(request):
    user = request.user
    visit_list = Visit.objects.filter(user=user).order_by('-when')[:50]
    return render(request, 'places/visit_list.html', {'visit_list': visit_list})


@login_required
def set_yelp(request, place_id, yelp_id):
    p = get_object_or_404(Place, id=place_id)
    if yelp_id != 'no_match':
        business = get_yelp_business(yelp_id)

        if business['name'] and business['url']:
            p.name = business['name']
            p.yelp = business['url']
            p.save()
    return place_detail(request, place_id)


@login_required
def select_yelp_match(request, p, yelp_matches):
    # print('There are {} yelp matches'.format(len(yelp_matches)), file=sys.stderr)
    return render(request, 'places/yelp_select.html',
                  {'place': p, 'yelp_list': yelp_matches})


@login_required
def place_add(request, pltype='rest'):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        if pltype == 'rest':
            form = RestaurantForm(request.POST)
        else:
            form = HotelForm(request.POST)
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

            p.good_for = d['good_for']
            p.comment = d['comment']
            p.dog_friendly = d['dog_friendly']

            if pltype == 'rest':
                p.pltype = Place.RESTAURANT
                p.cuisine = d['cuisine']
                p.yelp = d['yelp']
                p.outdoor = d['outdoor']
            else:
                p.pltype = Place.HOTEL
                p.yelp = d['tripadvisor']
                p.has_bar = d['has_bar']

            p.save()
            m = 'User: {} added place: {} with id: {}'.format(p.user, p.name, p.id)
            logprint(m)
            ChangeLog.place_add(p, request.user.username)

            if not p.yelp and p.pltype == Place.RESTAURANT:
                try:
                    yelp_matches = get_yelp_matches(p.name, p.city)
                    if yelp_matches:
                        return select_yelp_match(request, p, yelp_matches)
                except:
                    pass
            return place_detail(request, p.id)
    else:
        # form = PlaceForm().as_table()
        if pltype == 'rest':
            form = RestaurantForm().as_table()
        else:
            form = HotelForm().as_table()

    if pltype == 'rest':
        pltypeS = 'Restaurant'
    else:
        pltypeS = 'Hotel'
    return render(request, 'places/place_add.html', {'form': form, 'pltype': pltype,
                                                     'pltypeS': pltypeS})


@login_required
def place_share(request, place_id):
    p = get_object_or_404(Place, id=place_id)
    m = 'User: {} is sharing "{}"'.format(request.user.username, p.name)
    logprint(m)
    message = '''
Here is the {} I wanted to share with you.
It is called {} and it is in {}.
http://dev.trackplaces.com/places/view/{}/ - {}
'''.format(pltype_user_string(p), p.name, p.city, p.id, request.user.first_name)

    if request.method == 'POST':
        form = ShareForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            to_number = "+1" + data['to_number']
            from_number = data['from_number']
            message += "- reply to: {}".format(from_number)  # append from number
            ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
            AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
            client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
            try:
                client.messages.create(to=to_number, from_="+16692214546", body=message)
                m = 'Message sent to {} via twilio'.format(to_number)
                logprint(m)
                error_msg = False
            except twilio.TwilioRestException as e:
                m = 'Twilio returned error: {}'.format(e)
                logprint(m)
                error_msg = m

            return render(request, 'places/email_sent.html',
                          {'place': p, 'to': to_number, 'error': error_msg})
    else:
        form = ShareForm(initial={'subject': 'Place Information from TrackPlaces...'}).as_table()
    return render(request, 'places/share_form.html', {'form': form, 'p': p, 'msg': message})


@login_required
def place_copy(request, place_id):
    source = get_object_or_404(Place, id=place_id)

    place = Place(user=request.user,
                  name=source.name,
                  pltype=source.pltype,
                  city=source.city,
                  locale=source.locale,
                  cuisine=source.cuisine,
                  dog_friendly=source.dog_friendly,
                  has_bar=source.has_bar,
                  outdoor=source.outdoor,
                  yelp=source.yelp,
                  )

    place.id = Place.next_id()
    place.save()
    ChangeLog.place_copy(place, request.user.username, place_id)
    m = 'User: {} copied place: {}'.format(request.user, place.name)
    logprint(m)
    # because this is a new request it need a leading /
    return redirect('/places/edit/{}/'.format(place.id))


@login_required
def place_edit(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    pltypeS = pltype_user_string(place)
    init = {'name': place.name,
            'city': place.city,
            'locale': place.locale,
            'cuisine': place.cuisine,
            'outdoor': place.outdoor,
            'dog_friendly': place.dog_friendly,
            'has_bar': place.has_bar,
            'visited': place.visited,
            'rating': place.rating,
            'good_for': place.good_for,
            'comment': place.comment,
            'yelp': place.yelp,
            'tripadvisor': place.yelp}
    logprint('User: {} is editing place: {}'.format(request.user, place.name))
    if request.user == place.user:
        if place.pltype == Place.RESTAURANT:
            form = RestaurantForm(initial=init)
        else:
            form = HotelForm(initial=init)

        return render(request, 'places/place_edit.html',
                      {'p': place, 'form': form, 'pltypeS': pltypeS})
    else:
        return render(request, 'places/no_permission.html', {'p': place})


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
        elif k == 'has_bar':
            bool_val = (v == 'on')
            if p.has_bar != bool_val:
                p.has_bar = bool_val
                changed.append('has_bar')
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
        elif k == 'tripadvisor':
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

    if p.has_bar:
        if 'has_bar' not in args:
            p.has_bar = False
            changed.append('has_bar')

    if changed is not None:
        ChangeLog.place_edit(p, request.user.username)
        logprint('User: {} edited place: {}. Changed fields: {}'.format(request.user, p.name,
                                                                        ','.join(changed)))
        p.save()
    return place_detail(request, place_id)


def search(request, pltype='rest'):
    if request.method == 'GET':
        if pltype == 'rest':
            places = Place.restaurants.all()
        else:
            places = Place.hotels.all()
        args = {}
        logprint('User:{} is on search page'.format(request.user, args.get('pat', '')))
        ChangeLog.search(request.user.username)
    else:
        args = request.POST
        pat = re.compile(args['pat'], re.IGNORECASE)
        if pltype == 'rest':
            places = Place.restaurants.all()
        else:
            places = Place.hotels.all()
        places = [p for p in places
                  if pat.search(p.name) or pat.search(p.cuisine) or pat.search(p.city)]
        ChangeLog.search(request.user.username, args.get('pat', ''))
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
    places = sorted(places, key=lambda p: p.name.lower())

    return render(request, 'places/search.html',
                  {'places': places, 'args': args, 'pltype': pltype})


def delete(request, place_id):
    p = Place.objects.get(id=place_id)
    pltype = pltype_url_string(p)
    if request.method == 'GET':
        return render(request, 'places/confirm.html', {'place': p})
    else:
        args = request.POST
        answer = args['confirm']

        if answer == 'Yes':
            p.archived = True
            p.save()
            logprint('User: {} deleted place named: {}'.format(request.user, p.name))
            return city_list(request, pltype=pltype)
        else:
            return place_detail(request, p.id)


def about(request):
    logprint('User:{} is on about page'.format(request.user))
    return render(request, 'places/about.html')
