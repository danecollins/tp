from __future__ import print_function

from django.db import models


class Survey(models.Model):
    last = models.CharField(max_length=30, blank=True)

    @classmethod
    def get(cls):
        try:
            p = Survey.objects.get(id=1)
            s = p.last
        except:
            s = ''
        return s


class Vote(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    # men is False, women is True
    type = models.BooleanField(default=False, blank=True)
    survey = models.CharField(max_length=30, blank=True)
