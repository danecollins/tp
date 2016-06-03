# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0004_auto_20150521_1409'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='choice',
            field=models.CharField(max_length=20, blank=True),
        ),
    ]
