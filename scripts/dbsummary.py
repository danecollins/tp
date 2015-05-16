#!/Users/dane/env/dj/bin/python
import os
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
    message = 'There are %d users and %d places' % (len(u), len(p))
    url = 'https://hooks.slack.com/services/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'
    bot_name = 'tpserver'
    payload = {'text': message, 'username': bot_name, }
    r = requests.post(url, data=json.dumps(payload))

if __name__ == '__main__':
    summary()
