import os
import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from places.models import Place
import unittest


# tests find_partno_on_date by testing against total seats
class TestDataIntegrity(unittest.TestCase):

    def test_for_trailing_blanks(self):
        places = Place.objects.all()
        for p in places:
            self.assertEqual(p.name, p.name.strip())
            self.assertEqual(p.locale, p.locale.strip())
            self.assertEqual(p.city, p.city.strip())

    def test_yelp_links(self):
        places = Place.objects.all()
        for p in places:
            if p.yelp != '':
                self.assertTrue(p.yelp.startswith('http://'))

    def test_rating_range(self):
        places = Place.objects.all()
        for p in places:
            self.assertTrue(p.rating >= -1 and p.rating <= 3)

if __name__ == '__main__':
    unittest.main()
