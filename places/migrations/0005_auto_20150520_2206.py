# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0004_auto_20150518_2106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='opentable',
        ),
        migrations.RemoveField(
            model_name='place',
            name='want_to_go',
        ),
    ]
