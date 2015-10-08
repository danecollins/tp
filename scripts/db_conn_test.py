#!/Users/dane/env/dj/bin/python
import os
import django
from django.conf import settings
import requests
import json

import pprint
pp = pprint.PrettyPrinter(indent=4)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


def dbconntest():
    # pp.pprint(settings.DATABASES['default'])
    db = settings.DATABASES['default']
    host = db['HOST'] or 'localhost'
    print('host:    {}'.format(host))
    print('engine:  {}'.format(db['ENGINE']))
    print('name:    {}'.format(db['NAME']))

    print('pinging {}'.format(host))
    response = os.system("ping -c 1 " + host)

    #and then check the response...
    if response == 0:
      print(host, 'is up!')
    else:
      print(host, 'is down!')

if __name__ == '__main__':
    dbconntest()
