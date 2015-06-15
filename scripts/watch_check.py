#!/Users/dane/env/dj/bin/python
import os
import django
from django.conf import settings
import requests
import datetime
import pytz
import json
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from watch.models import Watcher, Event


def missing_events():
    watches = Watcher.objects.all()
    now = datetime.datetime.now()

    for w in watches:
        if w.active:
            delta = datetime.timedelta(hours=w.freq)
            expected = now - delta
            expected = pytz.UTC.localize(expected)
            last_event = Event.objects.filter(tag=w.tag).order_by('-id')[0]
            if last_event.time < expected:
                # get last event
                l = str(last_event.time)
                l = l.split(".")[0]
                msg = 'Missed event for watch "{}". Last seen: {}'.format(w.name, l)
                print(msg)
                url = 'https://hooks.slack.com/services/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'
                bot_name = 'watch4events'
                payload = {'text': msg, 'username': bot_name, }
                requests.post(url, data=json.dumps(payload))

if __name__ == '__main__':
    missing_events()
