import os
import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from places.models import Place
from django.contrib.auth.models import User
import unittest


# tests find_partno_on_date by testing against total seats
class TestDbIntegrity(unittest.TestCase):

    def test_number_of_records(self):
        places = Place.objects.all()
        self.assertTrue(len(places) > 25)

    def test_number_of_users(self):
        users = User.objects.all()
        self.assertTrue(len(users) > 1)


if __name__ == '__main__':
    unittest.main()
