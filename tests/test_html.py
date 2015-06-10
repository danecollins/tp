from __future__ import print_function
from __future__ import unicode_literals

import os

import django
from django.conf import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from django.test.client import Client

# import pdb
import unittest
from places.html_utils import ParsePage as PP

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

site_url = os.environ.get('TP_SITE_URL', 'http://localhost:8000')


def get_html(p):
    response = urlopen(site_url + p)
    text_anon = response.read()
    return text_anon


class TestHomePage(unittest.TestCase):
    url = '/'

    def test_page_title(self):
        html = get_html(self.url)
        self.assertEqual(PP.get_title(html), 'Welcome to Track Places')

    def test_menu_anon(self):
        html = get_html(self.url)
        # if not logged in there should be no logout link
        anon_menus = PP.menus.copy()
        del anon_menus['Logout']
        self.assertEqual(PP.get_menu_links(html), anon_menus)

    def test_buttons_anon(self):
        html = get_html(self.url)
        # should have buttons
        self.assertEqual(PP.get_button_links(html), PP.buttons)


class TestCityPage(unittest.TestCase):
    url = '/places/city/'

    def test_page_title(self):
        html = get_html(self.url)
        self.assertEqual(PP.get_title(html), 'TrackPlaces - Cities')

    def test_page_header(self):
        html = get_html(self.url)
        self.assertEqual(PP.get_header(html), 'Cities for Guest User')

    def test_city_links(self):
        html = get_html(self.url)
        anon_cities = PP.get_city_links(html)
        self.assertTrue(len(anon_cities) > 10)


class TestViewPlace(unittest.TestCase):
    '''Tests the place_details.html view'''
    url = '/places/view/107/'

    def test_page_title(self):
        html = get_html(self.url)
        self.assertEqual(PP.get_title(html), 'TrackPlaces - Details')

    def test_page_header(self):
        html = get_html(self.url)
        self.assertEqual(PP.get_header(html), 'Rock Bottom - Guest View')

    def test_page_content(self):
        html = get_html(self.url)
        # all the table fields are labelled with a class
        self.assertEqual(sorted(PP.anon_place_fields),
                         sorted(PP.get_place_fields(html)))

    def test_page_links(self):
        html = get_html(self.url)
        self.assertEqual(PP.get_button_links(html).keys(), PP.anon_place_buttons)

if __name__ == '__main__':
    unittest.main()
