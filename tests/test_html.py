from __future__ import print_function
from __future__ import unicode_literals

import os

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

        # the menu entries we want to check are about, blog and login
        menu_links = PP.get_menu_links(html)
        self.assertEqual(menu_links['About'], '/about/')
        self.assertEqual(menu_links['Blog'], '/blog/archive')
        self.assertEqual(menu_links['Login'], '/login?next=/places/rest/city')


    def test_buttons_anon(self):
        html = get_html(self.url)
        # should have buttons
        self.assertEqual(PP.get_button_links(html), PP.buttons)


class TestCityPage(unittest.TestCase):
    url = '/places/rest/city/'

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
        links = PP.get_button_links(html)
        # get just the button_text as a list
        button_text = list(links.keys())
        self.assertEqual(button_text, PP.anon_place_buttons)

if __name__ == '__main__':
    unittest.main()
