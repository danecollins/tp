# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0005_auto_20150520_2206'),
    ]

    operations = [
        migrations.RenameField(
            model_name='place',
            old_name='status',
            new_name='visited',
        ),
    ]
