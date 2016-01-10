# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0013_auto_20150815_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='when',
            field=models.DateField(),
        ),
    ]
