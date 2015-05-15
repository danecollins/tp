from __future__ import print_function
from __future__ import unicode_literals

import os
import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings_test")
django.setup()

import pdb
from bs4 import BeautifulSoup
import unittest

from django.test.client import Client

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

site_url = 'http://localhost:8000'


# Utility Functions
menus = {
    u'Home': u'/',
    u'Add Place': u'/places/add',
    u'Search': u'/places/search',
    u'About': u'/about/',
    u'Blog': u'/blog/archive',
    u'Logout': u'/logout?next=/',
    u'Cities': u'/places/city'
}

anon_place_fields = [u'City', u'Locale', u'Cuisine',
                     u'Outdoor Seating', u'Dog Friendly']

user_place_fields = [u'City', u'Locale', u'Cuisine',
                     u'Outdoor Seating', u'Dog Friendly',
                     u'Rating', u'Good For', u'Comment']

def get_menu_links(soup):
    l = {}
    for a in soup.find_all('a', class_="pure-menu-link"):
        l[a.text] = a['href']
    return l


buttons = {
    u'Login': u'/login',
    u'Register': u'/newuser',
    u'Use As Guest': u'/places/city'
}


def get_button_links(soup):
    l = {}
    for a in soup.find_all('a', class_='pure-button'):
        l[a.text] = a['href']
    return l


def get_anon_page(p, c):
    # make sure we're logged out
    c.get('/logout')
    response = c.get(p)
    text_anon = response.content
    soup_anon = BeautifulSoup(text_anon)
    return soup_anon


def get_user_page(p, c):
    response = c.post('/login/', {'username': 'cindy', 'password': 'sjsharks'})
    response = c.get(p)
    text_user = response.content
    soup_user = BeautifulSoup(text_user)
    return soup_user


def get_page_variants(p):
    c = Client()
    soup_anon = get_anon_page(p, c)
    soup_user = get_user_page(p, c)
    return (soup_anon, soup_user)



class TestHomePage(unittest.TestCase):
    url = '/'

    def test_page_title(self):
        (anon, user) = get_page_variants(self.url)
        self.assertEqual(anon.title.text, 'Welcome to Track Places')
        self.assertEqual(user.title.text, 'Welcome to Track Places')

    def test_menu_anon(self):
        (anon, user) = get_page_variants(self.url)
        # if not logged in there should be no logout link
        anon_menus = menus.copy()
        del anon_menus['Logout']
        self.assertEqual(get_menu_links(anon), anon_menus)

    def test_menu_user(self):
        (anon, user) = get_page_variants(self.url)
        self.assertEqual(get_menu_links(user), menus)

    def test_buttons_anon(self):
        (anon, user) = get_page_variants(self.url)
        # should have buttons
        self.assertEqual(get_button_links(anon), buttons)

    def test_buttons_user(self):
        (anon, user) = get_page_variants(self.url)
        # if logged in there hsould be no buttons
        self.assertEqual(get_button_links(user), {})


class TestCityPage(unittest.TestCase):
    url = '/places/city/'

    def test_page_title(self):
        (anon, user) = get_page_variants(self.url)
        self.assertEqual(anon.title.text, 'TrackPlaces - Cities')
        self.assertEqual(user.title.text, 'TrackPlaces - Cities')

    def test_page_header(self):
        (anon, user) = get_page_variants(self.url)
        self.assertEqual(anon.body.div.h1.text, 'Cities for Guest User')
        self.assertEqual(user.body.div.h1.text, 'Cities for Cindy')

    def test_city_links(self):
        (anon, user) = get_page_variants(self.url)
        anon_cities = anon.find_all('a', class_='city-link')
        self.assertTrue(len(anon_cities) > 10)
        user_cities = user.find_all('a', class_='city-link')
        self.assertTrue(len(user_cities) == 2)


class TestViewPlace(unittest.TestCase):
    url = '/places/view/107/'

    def test_page_title(self):
        (anon, user) = get_page_variants(self.url)
        self.assertEqual(anon.title.text, 'TrackPlaces - Details')
        self.assertEqual(user.title.text, 'TrackPlaces - Details')

    def test_page_header(self):
        (anon, user) = get_page_variants(self.url)
        self.assertEqual(anon.body.div.h3.text, 'Rock Bottom - Guest View')
        self.assertEqual(user.body.div.h3.text, 'Rock Bottom')

    def test_page_content(self):
        (anon, user) = get_page_variants(self.url)
        li_items = anon.find_all('li', class_='place-field')
        fields = [x.text.split(':')[0] for x in li_items]
        self.assertEqual(fields, anon_place_fields)
        li_items = user.find_all('li', class_='place-field')
        fields = [x.text.split(':')[0] for x in li_items]
        self.assertEqual(fields, user_place_fields)

        self.assertEqual(get_button_links(anon), {})
        user_buttons = get_button_links(user)
        desired = {u'Edit Restaurant Information': u'/places/edit/107',
                   u'Share': u'/places/share/107'}
        self.assertEqual(user_buttons, desired)

if __name__ == '__main__':
    unittest.main()
