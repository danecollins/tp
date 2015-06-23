# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0008_changelog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='changelog',
            name='action',
        ),
        migrations.RemoveField(
            model_name='changelog',
            name='place',
        ),
        migrations.RemoveField(
            model_name='changelog',
            name='user',
        ),
        migrations.AddField(
            model_name='changelog',
            name='message',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
