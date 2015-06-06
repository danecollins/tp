#!/Users/dane/env/dj/bin/python
from __future__ import print_function
from __future__ import unicode_literals
import os
os.environ['DATABASE_URL'] = os.environ['HPG_PROD_URL']
import django
from django.conf import settings
import requests
import json
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from places.models import Place
from django.contrib.auth.models import User


def summary():
    u = User.objects.all()
    p = Place.objects.all()
    print('There are %d users and %d places' % (len(u), len(p)))
    for place in p:
        if place.yelp == '' and place.archived != True:
            print('%s (%d) is missing yelp link' % (place.name, place.id))

if __name__ == '__main__':
    summary()
