# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('tag', models.CharField(max_length=30)),
                ('log_type', models.CharField(default=b'LOG', max_length=3, choices=[(b'LOG', b'Log'), (b'NOT', b'Notification')])),
            ],
        ),
        migrations.CreateModel(
            name='Watcher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('tag', models.CharField(max_length=8)),
                ('freq', models.IntegerField()),
            ],
        ),
    ]
