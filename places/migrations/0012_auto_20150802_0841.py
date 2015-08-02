# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0011_auto_20150704_0819'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='has_bar',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='place',
            name='pltype',
            field=models.CharField(default=b'R', max_length=1, choices=[(b'R', b'R'), (b'H', b'H')]),
        ),
    ]
