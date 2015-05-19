# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0003_place_cuisine'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='archived',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='place',
            name='opentable',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='place',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
