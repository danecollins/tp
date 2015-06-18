import os

from places.models import Place
import unittest


# tests find_partno_on_date by testing against total seats
class TestDataIntegrity(unittest.TestCase):

    def test_for_trailing_blanks(self):
        places = Place.objects.all()
        for p in places:
            self.assertEqual(p.name, p.name.strip(),
                             msg='name {} contains spaces'.format(p.name))
            self.assertEqual(p.locale, p.locale.strip(),
                             msg='locale {} on place {} has spaces'.format(p.locale, p.name))
            self.assertEqual(p.city, p.city.strip(),
                             msg='city {} on place {} has spaces'.format(p.city, p.name))

    def test_yelp_links(self):
        places = Place.objects.all()
        for p in places:
            if p.yelp != '':
                self.assertTrue(p.yelp.startswith('http://'))

    def test_rating_range(self):
        places = Place.objects.all()
        for p in places:
            self.assertTrue(p.rating >= 0 and p.rating <= 3,
                            msg='rating {} out of range on place {}'.format(p.rating, p.name))

if __name__ == '__main__':
    unittest.main()
