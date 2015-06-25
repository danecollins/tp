# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0009_auto_20150623_0936'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 24, 4, 6, 20, 867670, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
