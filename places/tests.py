from django.test import TestCase

# Create your tests here.
from places.models import City, Locale, Place, UserInfo
from django.contrib.auth.models import User
import pdb

def username(n):
    return 'test{}'.format(n)


def create_users():
    u = User(username=username(1))
    u.save()
    u = User(username=username(2))
    u.save()


def create_campbell(u):
    c = City(name='Campbell', user=u)
    c.save()
    return c


def create_santacruz(u):
    c = City(name='Santa Cruz', user=u)
    c.save()
    return c


def create_sanjose(u):
    c = City(name='San Jose', user=u)
    c.save()
    return c


def create_places():
    create_users()
    ca = create_campbell(user(1))
    sc = create_santacruz(user(1))
    l1 = Locale(name='Harbor', city=sc, user=user(1))
    l1.save()
    l2 = Locale(name='Downtown', city=ca, user=user(1))
    l2.save()
    p = Place(name='Engfer Pizza',
              user=user(1),
              locale=l1,
              outdoor=True,
              dog_friendly=True)
    p.save()
    p = Place(name='Seabright Brewery',
              user=user(1),
              locale=l1,
              outdoor=True,
              dog_friendly=True)
    p.save()
    p = Place(name='Bucca di Beppo',
              user=user(1),
              locale=l2,
              outdoor=False,
              dog_friendly=False)
    p.save()


def user(n):
    return User.objects.get(username=username(n))


class TestUtility(TestCase):
    def test_username(self):
        self.assertEqual(username(1), 'test1')
        self.assertEqual(username(2), 'test2')

    def test_create_users(self):
        create_users()
        u1 = user(1)
        self.assertEqual(u1.username, username(1))
        u2 = user(2)
        self.assertEqual(u2.username, username(2))


class TestCity(TestCase):
    def test_city_create_1(self):
        create_users()
        create_campbell(user(1))
        self.assertEqual(len(City.objects.all()), 1)

    def test_city_create_2(self):
        create_users()
        create_campbell(user(1))
        create_santacruz(user(1))
        self.assertEqual(len(City.objects.all()), 2)
        create_campbell(user(2))
        create_santacruz(user(2))
        self.assertEqual(len(City.objects.all()), 4)


class TestLocale(TestCase):
    def test_locale_create(self):
        create_users()
        ca = create_campbell(user(1))
        sj = create_sanjose(user(1))
        l1 = Locale(name='Downtown', city=ca, user=user(1))
        l1.save()
        l2 = Locale(name='Downtown', city=sj, user=user(1))
        l2.save()
        self.assertEqual(len(Locale.objects.all()), 2)

    def test_place_from_locale(self):
        create_places()
        l1 = Locale.objects.get(name='Harbor')
        places = l1.place_set.all()
        self.assertEqual(len(places), 2)
        names = [x.name for x in places]
        self.assertEqual(names, ['Engfer Pizza',
                                 'Seabright Brewery'])


class TestPlace(TestCase):
    def test_place_create(self):
        create_places()
        self.assertEqual(len(Place.objects.all()), 3)

    def test_place_filter(self):
        create_places()
        outdoor = Place.objects.filter(outdoor=True)
        self.assertEqual(len(outdoor), 2)
        self.assertEqual(outdoor[0].name, 'Engfer Pizza')
        self.assertEqual(outdoor[0].user.username, username(1))
        u2 = Place.objects.filter(user=user(2))
        self.assertEqual(len(u2), 0)


class TestUserInfo(TestCase):
    def test_user_info_create(self):
        create_places()
        p = Place.objects.get(name='Engfer Pizza')
        ui = UserInfo(user=user(1),
                      place=p,
                      rating=1,
                      comment='Only open for dinner')
        ui.save()
        self.assertEqual(len(UserInfo.objects.all()), 1)

    def test_user_info_from_place(self):
        create_places()
        p = Place.objects.get(name='Engfer Pizza')
        ui = UserInfo(user=user(1),
                      place=p,
                      rating=1,
                      comment='Only open for dinner')
        ui.save()

        ui = p.userinfo_set.all()
        self.assertEqual(len(ui), 1, msg='UserInfo not found')
        ui = ui[0]
        self.assertEqual(ui.rating, 1)
        self.assertEqual(ui.comment, 'Only open for dinner')
