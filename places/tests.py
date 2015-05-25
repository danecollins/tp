from django.test import TestCase, Client

# Create your tests here.
from .models import Place
from .forms import PlaceForm
from .html_utils import ParsePage as PP
from django.contrib.auth.models import User
import pdb


def username(n):
    return 'test{}'.format(n)


def get_user(n):
    return User.objects.get(username=username(n))


def create_users():
    u = User.objects.create_user(username=username(1), password='password', first_name='Test', last_name='User')
    u.save()
    u = User.objects.create_user(username=username(2), password='password')
    u.save()


def create_engfer(user):
    p = Place(
        user=get_user(user),
        name='Engfer Pizza',
        locale='Harbor',
        city='Santa Cruz',
        outdoor=True,
        rating=3,
        dog_friendly=True,
        visited=1,
        good_for='casual dinner',
        comment='only open at dinner')
    p.save()
    return(p)


def create_johnnys(user):
    p = Place(
        user=get_user(user),
        name="Johnny's",
        locale='Harbor',
        city='Santa Cruz',
        outdoor=False,
        rating=2,
        dog_friendly=False,
        visited=1,
        good_for='fancy dinner',
        comment='good seafood')
    p.save()
    return(p)


def create_campbell():
    user = get_user(1)
    for s in campbell_restaurants:
        Place.from_csv(user, s)


def create_sanjose():
    user = get_user(1)
    for s in sanjose_restaurants:
        Place.from_csv(user, s)


def create_some_places():
    create_users()
    create_engfer(1)
    create_johnnys(1)
    create_engfer(2)


campbell_restaurants = [
    "Aqui Cal-Mex,Downtown,Campbell,1,1,2,0,Swirls,",
    "Bellagio,Downtown,Campbell,0,0,1,0,,",
    "Blue Line Pizza,Downtown,Campbell,1,1,2,0,,deep dish pizza",
    "Buca di Beppo,Pruneyard,Campbell,0,0,1,0,big groups,"]

sanjose_restaurants = [
    "Mama Mia's,Westgate,San Jose,1,1,2,0,Swirls,",
    "Capers,Out-of-Town,San Jose,0,0,1,0,,",
    "Willow Street,Westgate,San Jose,1,1,2,0,,deep dish pizza",
    "Tomatina,Westgate,San Jose,0,0,1,0,big groups,"]


def create_many_places():
    create_campbell()


def create_all_places():
    create_campbell()
    create_sanjose()


class TestUtility(TestCase):
    def test_username(self):
        self.assertEqual(username(1), 'test1')
        self.assertEqual(username(2), 'test2')

    def test_create_users(self):
        create_users()
        u1 = get_user(1)
        self.assertEqual(u1.username, username(1))
        u2 = get_user(2)
        self.assertEqual(u2.username, username(2))


class TestModels(TestCase):
    def test_simple_create(self):
        create_users()
        create_engfer(1)
        self.assertEqual(len(Place.objects.all()), 1)
        create_johnnys(1)
        self.assertEqual(len(Place.objects.all()), 2)
        create_engfer(2)
        self.assertEqual(len(Place.objects.all()), 3)

    def test_create_some_places(self):
        create_some_places()
        self.assertEqual(len(Place.objects.all()), 3)
        # make sure there are 2 users
        p = Place.objects.all()
        users = set([x.user.username for x in p])
        self.assertEqual(len(users), 2, msg='Wrong users: {}'.format(users))

    def test_place_filter(self):
        create_some_places()
        outdoor = Place.objects.filter(outdoor=True)
        self.assertEqual(len(outdoor), 2)
        self.assertEqual(outdoor[0].name, 'Engfer Pizza')
        self.assertEqual(outdoor[0].user.username, username(1))
        u2 = Place.objects.filter(user=get_user(2))
        self.assertEqual(len(u2), 1)

    def test_create_many_places(self):
        create_users()
        create_many_places()
        n = len(Place.objects.all())
        self.assertTrue(n > 3, msg='There are only {} places in db'.format(n))

    def test_create_from_file(self):
        create_users()
        fn = '/Users/dane/src/tp/places/initial.txt'
        Place.from_file(get_user(1), fn)
        self.assertEqual(len(Place.objects.all()), 102)

#############################################################################
#
# Form Tests
#

add_form_labels = ['Name', 'City', 'Locale', 'Cuisine', 'Outdoor Seating', 'Dog Friendly',
                   'Visit Type', 'Rating', 'Good For', 'Comment', 'Yelp URL']


class TestForms(TestCase):
    def test_place_form(self):
        p = PlaceForm()
        html = p.as_table()
        field_labels = sorted(PP.get_place_labels(html))
        should_be = sorted([x + ":" for x in add_form_labels])
        self.assertEqual(field_labels, should_be)

#############################################################################
#
# View Tests
#


def get_anon_page(p, c):
    # make sure we're logged out
    c.get('/logout')
    response = c.get(p)
    text_anon = response.content
    return text_anon


def get_user_page(p, c):
    response = c.post('/login/', {'username': 'test1', 'password': 'password'})
    response = c.get(p)
    text_user = response.content
    return text_user


def get_page_variants(p):
    c = Client()
    text_anon = get_anon_page(p, c)
    text_user = get_user_page(p, c)
    return (text_anon, text_user)


class TestViewHome(TestCase):
    url = '/'

    def test_page_title(self):
        create_users()
        (anon, user) = get_page_variants(self.url)
        self.assertEqual(PP.get_title(anon), 'Welcome to Track Places')
        self.assertEqual(PP.get_title(user), 'Welcome to Track Places')

    def test_menu_anon(self):
        create_users()
        (anon, user) = get_page_variants(self.url)
        # if not logged in there should be no logout link
        anon_menus = PP.menus.copy()
        del anon_menus['Logout']
        self.assertEqual(PP.get_menu_links(anon), anon_menus)

    def test_menu_user(self):
        create_users()
        (anon, user) = get_page_variants(self.url)
        self.assertEqual(PP.get_menu_links(user), PP.menus)

    def test_buttons_anon(self):
        create_users()
        (anon, user) = get_page_variants(self.url)
        # should have buttons
        self.assertEqual(PP.get_button_links(anon), PP.buttons)

    def test_buttons_user(self):
        create_users()
        (anon, user) = get_page_variants(self.url)
        # if logged in there hsould be no buttons
        self.assertEqual(PP.get_button_links(user), {})


class TestViewCityList(TestCase):
    url = '/places/city/'

    def test_page_title(self):
        create_users()
        (anon, user) = get_page_variants(self.url)
        self.assertEqual(PP.get_title(anon), 'TrackPlaces - Cities')
        self.assertEqual(PP.get_title(user), 'TrackPlaces - Cities')

    def test_page_header(self):
        create_users()
        (anon, user) = get_page_variants(self.url)
        self.assertEqual(PP.get_header(anon), 'Cities for Guest User')
        self.assertEqual(PP.get_header(user), 'Cities for Test')

    def test_city_links(self):
        create_users()
        create_all_places()
        (anon, user) = get_page_variants(self.url)
        anon_cities = PP.get_city_links(anon)
        self.assertEqual(len(anon_cities), 2)
        user_cities = PP.get_city_links(user)
        self.assertEqual(len(user_cities), 2)


class TestViewPlaceDetail(TestCase):
    '''Tests the place_details.html view'''
    def get_url(self):
        place = Place.objects.get(name='Blue Line Pizza')
        #
        # MUST HAVE A TRAILING / OR ELSE GET A REDIRECT ERROR !!!!!!!!!!!!!!!!!!!!!
        url = '/places/view/{}/'.format(place.id)
        return url

    def test_page_title(self):
        create_users()
        create_all_places()
        (anon, user) = get_page_variants(self.get_url())
        self.assertEqual(PP.get_title(anon), 'TrackPlaces - Details')
        self.assertEqual(PP.get_title(user), 'TrackPlaces - Details')

    def test_page_header(self):
        create_users()
        create_all_places()
        (anon, user) = get_page_variants(self.get_url())
        self.assertEqual(PP.get_header(anon), 'Blue Line Pizza - Guest View')
        self.assertEqual(PP.get_header(user), 'Blue Line Pizza')

    def test_page_fields(self):
        create_users()
        create_all_places()
        (anon, user) = get_page_variants(self.get_url())
        self.assertEqual(sorted(PP.anon_place_fields),
                         sorted(PP.get_place_fields(anon)))
        self.assertEqual(sorted(PP.user_place_fields),
                         sorted(PP.get_place_fields(user)))

    def test_page_button_links(self):
        create_users()
        create_all_places()
        (anon, user) = get_page_variants(self.get_url())
        self.assertEqual(PP.get_button_links(anon), {})
        user_buttons = PP.get_button_links(user)
        self.assertTrue(user_buttons['Edit Restaurant Information'].startswith('/places/edit'))
        self.assertTrue(user_buttons['Share'].startswith('/places/share'))
