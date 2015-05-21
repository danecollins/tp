# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0002_auto_20150519_1901'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vote',
            old_name='problem',
            new_name='survey',
        ),
    ]
