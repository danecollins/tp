from django.db import models

# Create your models here.
from django.db import models


class Vote(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    # men is False, women is True
    type = models.BooleanField(default=False, blank=True)
