"""
Django Testing settings for tp project.

"""

import os
from config.settings import *
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', '0') == '1'

TEMPLATE_DEBUG = os.environ.get('DJANGO_DEBUG', '0') == '1'

try:
    db = os.environ['DB']
    assert(db=='tpdata' or db=='tpdata_test')
except:
    print('Must set which db to use.  export DB=[tpdata|tpdata_test]')
    exit(1)

os.environ['DATABASE_URL'] = 'postgres:///{}'.format(db)
DATABASES['default'] = dj_database_url.config()
