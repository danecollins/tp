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


def create_santacruz(u):
    c = City(name='Santa Cruz', user=u)
    c.save()


def create_sanjose(u):
    c = City(name='San Jose', user=u)
    c.save()


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


# class TestCityClass(TestCase):
#     def test_city_create_1(self):
#         create_users()
#         create_campbell(get_u1())
#         self.assertEqual(len(City.objects.all()), 1)

#     def test_city_create_2(self):
#         create_users()
#         create_campbell(user(1))
#         create_santacruz(user(1))
#         self.assertEqual(len(City.objects.all()), 2)
#         create_campbell(user(2))
#         create_santacruz(user(2))
#         self.assertEqual(len(City.objects.all()), 4)
