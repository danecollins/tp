from django.db import models
from django.contrib.auth.models import User
import os


class VisitType:
    WantToGo = 0
    HaveBeenTo = 1
    NotInterested = 2
    DontGoAgain = 3

    @classmethod
    def type_list(cls):
        tup = list()
        for i in range(4):
            tup.append((i, cls.as_string(i)))
        return tup

    @classmethod
    def as_string(cls, int_value):
        if int_value == cls.WantToGo:
            return 'Want To Go To'
        elif int_value == cls.HaveBeenTo:
            return 'Have Been To'
        elif int_value == cls.DontGoAgain:
            return "Don't Go Back"
        elif int_value == cls.NotInterested:
            return 'Not Interested'
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
    good_for = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=200, blank=True)
    yelp = models.CharField(max_length=200, blank=True)
    archived = models.BooleanField(default=False, blank=True)
    visited = models.IntegerField(default=0)

    # This is required so that we can log the event
    @classmethod
    def from_args(cls, *args, **kwargs):
        obj = cls(*args, **kwargs)
        obj.save()
        return obj

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
        self.visited = fields[6] == '1'
        self.good_for = fields[7]
        self.comment = fields[8]
        self.save()
        return self

    @classmethod
    def next_id(cls):
        places = cls.objects.all()
        if len(places) > 0:
            largest_id = max([x.id for x in cls.objects.all()])
            return (largest_id + 1)
        else:
            return 0

    @classmethod
    def last_added(cls):
        places = cls.objects.all()
        if places.exists():
            largest_id = max([x.id for x in places])
            return Place.objects.get(id=largest_id)
        else:
            # create a dummy object for the tests to run
            p = {'name': 'Dummy Place', 'city': 'Dummy City', 'cuisine': 'Other',
                 'user': {'first_name': 'Dummy'}}
            return p

    @classmethod
    def from_file(cls, user, fn):
        assert os.path.exists(fn)
        print(fn)
        with open(fn, 'U') as fp:  # need 'U' for 2.7 compatibility
            fp.readline()  # skip header
            for line in fp.readlines():
                cls.from_csv(user, line, delimiter='\t')

    def __str__(self):
        return '{} at the {} in {}'.format(self.name, self.locale, self.city)

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
        s += 'visited="{}",'.format(self.visited)
        s += 'good_for="{}",'.format(self.good_for)
        s += 'comment="{}",'.format(self.comment)
        s += 'yelp="{}"'.format(self.yelp)
        s += ')'
        return s

    class Meta:
        app_label = 'places'


class Visit(models.Model):
    when = models.DateField(auto_now_add=True)
    place = models.ForeignKey(Place)
    user = models.ForeignKey(User)

    @classmethod
    def last_visit(cls, place, user):
        visits = cls.objects.filter(place=place, user=user)
        if visits.exists():
            visit = sorted(visits, key=lambda x: x.when)
            return visit[0]
        else:
            return None

    class Meta:
        app_label = 'places'


class ChangeLog(models.Model):
    when = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=100)

    @classmethod
    def create_user(cls, user):
        msg = 'Create user "{}"'.format(user.username)
        cls(message=msg).save()

    @classmethod
    def get_create_user(cls):
        return cls.objects.filter(message__startswith='Create user')

    @classmethod
    def create_place(cls, place):
        msg = '"{}" created place named "{}"'.format(place.user.username, place.name)
        cls(message=msg).save()

    @classmethod
    def get_create_place(cls):
        return cls.objects.filter(message__contains='created place named')

    def view_city_list(cls, username="anonymous"):
        msg = '"{}" viewed the city list'.format(username)
        cls(message=msg).save()

    def __str__(self):
        return '{}: {}'.format(self.when, self.message)

    class Meta:
            app_label = 'places'
