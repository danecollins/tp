# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('places', '0007_visit'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChangeLog',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField(auto_now_add=True)),
                ('action', models.CharField(max_length=12, choices=[('CreateUser', 'created a User'), ('CreatePlace', 'created a Place'), ('ViewPlace', 'viewed a Place'), ('EditPlace', 'edited a Place'), ('AddVisit', 'added a Visit')])),
                ('place', models.ForeignKey(to='places.Place', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
