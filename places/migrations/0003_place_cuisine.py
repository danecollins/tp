# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0002_place_yelp'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='cuisine',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
