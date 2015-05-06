from django.test import TestCase

# Create your tests here.
from places.models import Place
from django.contrib.auth.models import User
import pdb


def username(n):
    return 'test{}'.format(n)


def get_user(n):
    return User.objects.get(username=username(n))


def create_users():
    u = User(username=username(1))
    u.save()
    u = User(username=username(2))
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
        want_to_go=False,
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
        want_to_go=False,
        good_for='fancy dinner',
        comment='good seafood')
    p.save()
    return(p)


def create_campbell():
    user = get_user(1)
    for s in campbell_restaurants:
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


def create_many_places():
    create_campbell()


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


class TestPlace(TestCase):
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
