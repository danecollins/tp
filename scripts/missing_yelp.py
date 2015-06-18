#!/Users/dane/env/dj/bin/python
from __future__ import print_function
from __future__ import unicode_literals
import os

from places.models import Place
from django.contrib.auth.models import User
import config.settings


def summary():
    u = User.objects.all()
    p = Place.objects.filter()

    print('\nUsing database: {}\n'.format(config.settings.DATABASES['default']['NAME']))
    print('There are %d users and %d places' % (len(u), len(p)))
    for place in p:
        if place.yelp == '' and place.archived != True:
            print('%s (%d) is missing yelp link' % (place.name, place.id))

if __name__ == '__main__':
    summary()
