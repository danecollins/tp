# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('watch', '0002_watcher_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='log_type',
            field=models.CharField(default='LOG', max_length=3, choices=[('LOG', 'Log'), ('NOT', 'Notification')]),
        ),
    ]
