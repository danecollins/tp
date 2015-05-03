# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('locale', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('outdoor', models.BooleanField(default=False)),
                ('dog_friendly', models.BooleanField(default=False)),
                ('rating', models.IntegerField(default=0)),
                ('want_to_go', models.BooleanField(default=False)),
                ('good_for', models.CharField(blank=True, max_length=50)),
                ('comment', models.CharField(blank=True, max_length=200)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
