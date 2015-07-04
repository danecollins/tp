# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0010_place_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='changelog',
            name='message',
            field=models.CharField(max_length=130),
        ),
    ]
