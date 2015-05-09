from django.db import models
from django.contrib.auth.models import User
import os
import pdb


class Place(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    locale = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    outdoor = models.BooleanField(default=False, blank=True)
    dog_friendly = models.BooleanField(default=False, blank=True)
    rating = models.IntegerField(default=0)
    want_to_go = models.BooleanField(default=False, blank=True)
    good_for = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=200, blank=True)
    yelp = models.CharField(max_length=200, blank=True)

    @classmethod
    def from_csv(cls, user, text, delimiter=','):
        self = cls()
        fields = text.split(delimiter)
        fields = [x.strip("'") for x in fields]
        if len(fields) != 12:
            print('ERROR: invalid fields in from_csv. got {} should be 12'.format(len(fields)))
            print(fields)
            return None

        self.id = fields[0]
        self.user = User.objects.get(id=fields[11])
        self.yelp = fields[1]
        self.name = fields[2]
        self.locale = fields[3]
        self.city = fields[4]
        self.outdoor = fields[5] == '1'
        self.dog_fiendly = fields[6] == '1'
        self.rating = fields[7]
        self.want_to_go = fields[8] == '1'
        self.good_for = fields[9]
        self.comment = fields[10]
        self.save()
        return self

    @classmethod
    def from_file(cls, user, fn):
        assert os.path.exists(fn)
        print(fn)
        with open(fn, 'U') as fp:  # need 'U' for 2.7 compatibility
            #fp.readline()  # skip header
            for line in fp.readlines():
                line = line.strip()
                cls.from_csv(user, line)

    def __str__(self):
        return '{} at the {} in {}'.format(self.name, self.locale, self.locale.city)

    def __repr__(self):
        s = 'Place('
        s += 'user={},'.format(self.user.__repr__())
        s += 'name="{}",'.format(self.name)
        s += 'locale="{}",'.format(self.locale)
        s += 'city="{}",'.format(self.city)
        s += 'outdoor="{}",'.format(self.outdoor)
        s += 'dog_friendly="{}",'.format(self.dog_friendly)
        s += 'rating="{}",'.format(self.rating)
        s += 'want_to_go="{}",'.format(self.want_to_go)
        s += 'good_for="{}",'.format(self.good_for)
        s += 'comment="{}",'.format(self.comment)
        s += 'yelp="{}"'.format(self.yelp)
        s += ')'
        return s

    class Meta:
        app_label = 'places'
