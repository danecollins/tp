#!/Users/dane/env/dj/bin/python
import os
import sys
import django
from django.conf import settings
from django.utils import timezone
import requests
import datetime
import pytz
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from watch.models import Watcher, Event

# everything in UTC since that is what is in the database
utc = pytz.UTC

def missing_events(debug=False):
    watches = Watcher.objects.all()
    now = timezone.now()

    for w in watches:
        if w.active:
            delta = datetime.timedelta(hours=w.freq)
            expected = now - delta
            last_event = Event.objects.filter(tag=w.tag).order_by('-id')[0]
            if last_event:
                last_time = last_event.time
            if last_time < expected:
                # get last event
                l = str(last_time)
                l = l.split(".")[0]
                msg = 'Missed event for watch "{}". Last seen: {}'.format(w.name, l)
                print(msg)
                url = 'https://hooks.slack.com/services/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'
                bot_name = 'watch4events'
                payload = {'text': msg, 'username': bot_name, }
                if not debug:
                    requests.post(url, data=json.dumps(payload))
            else:
                if debug:
                    print('Last "{}"'.format(w.name))
                    print('    expected: {}'.format(expected))
                    print('    occurred: {}'.format(last_time))

if __name__ == '__main__':
    if len(sys.argv) == 2:
        missing_events(debug=True)
    else:
        missing_events(debug=False)
