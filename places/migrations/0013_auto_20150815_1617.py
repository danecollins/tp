# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0012_auto_20150802_0841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='pltype',
            field=models.CharField(default=b'R', max_length=1, choices=[(b'R', b'Restaurant'), (b'H', b'Hotel')]),
        ),
    ]
