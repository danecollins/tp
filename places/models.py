from django.db import models
from django.contrib.auth.models import User
import os


class Status:
    WantToGo = 1
    DontGoAgain = -1
    HaveNotBeenTo = 0
    HaveBeenTo = 2

    @classmethod
    def as_string(cls,int_value):
        if int_value == 1:
            return 'Want To Go To'
        elif int_value == 0:
            return 'Have Not Been To'
        elif int_value == -1:
            return "Don't Go Again"
        elif int_value == 2:
            return 'Have Been To'
        else:
            return 'Illegal Value'


class Place(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    locale = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    cuisine = models.CharField(max_length=100, blank=True)
    outdoor = models.BooleanField(default=False, blank=True)
    dog_friendly = models.BooleanField(default=False, blank=True)
    rating = models.IntegerField(default=0)
    want_to_go = models.BooleanField(default=False, blank=True)
    good_for = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=200, blank=True)
    yelp = models.CharField(max_length=200, blank=True)
    opentable = models.CharField(max_length=200, blank=True)
    archived = models.BooleanField(default=False, blank=True)
    status = models.IntegerField(default=0)


    @classmethod
    def from_csv(cls, user, text, delimiter=','):
        # create a place from a csv string
        # field order is:
        #   0 - place name   string
        #   1 - locale       string
        #   2 - city         string
        #   3 - outdoor      0 or 1
        #   4 - dog_friendly 0 or 1
        #   5 - rating       0 if unset, 1-3 otherwise
        #   6 - want_to_go   0 or 1
        #   7 - good_for     string
        #   8 - comment      string
        #
        self = cls()
        fields = text.split(delimiter)
        if len(fields) != 9:
            print('ERROR: invalid fields in from_csv. got {} should be 9'.format(len(fields)))
            print(fields)
            return None

        self.user = user
        self.name = fields[0]
        self.locale = fields[1]
        self.city = fields[2]
        self.outdoor = fields[3] == '1'
        self.dog_fiendly = fields[4] == '1'
        self.rating = fields[5]
        self.want_to_go = fields[6] == '1'
        self.good_for = fields[7]
        self.comment = fields[8]
        self.save()
        return self

    @classmethod
    def from_file(cls, user, fn):
        assert os.path.exists(fn)
        print(fn)
        with open(fn, 'U') as fp:  # need 'U' for 2.7 compatibility
            fp.readline()  # skip header
            for line in fp.readlines():
                cls.from_csv(user, line, delimiter='\t')

    def __str__(self):
        return '{} at the {} in {}'.format(self.name, self.locale, self.locale.city)

    def __repr__(self):
        s = 'Place('
        s += 'user={},'.format(self.user.__repr__())
        s += 'name="{}",'.format(self.name)
        s += 'locale="{}",'.format(self.locale)
        s += 'city="{}",'.format(self.city)
        s += 'cuisine="{}"'.format(self.cuisine)
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
