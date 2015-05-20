# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last', models.CharField(max_length=30, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='vote',
            name='problem',
            field=models.CharField(max_length=30, blank=True),
        ),
    ]
