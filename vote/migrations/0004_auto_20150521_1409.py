# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0003_auto_20150521_1407'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Problem',
            new_name='Survey',
        ),
    ]
