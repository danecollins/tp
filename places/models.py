from django.db import models
from django.contrib.auth.models import User


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

    @classmethod
    def from_csv(cls, text, delimiter=','):
        # create a place from a csv string
        # field order is:
        #   0 - username     string
        #   1 - place name   string
        #   2 - locale       string
        #   3 - city         string
        #   4 - outdoor      0 or 1
        #   5 - dog_friendly 0 or 1
        #   6 - rating       0 if unset, 1-3 otherwise
        #   7 - want_to_go   0 or 1
        #   8 - good_for     string
        #   9 - comment      string
        #
        self = cls()
        fields = text.split(delimiter)
        if len(fields) != 10:
            print('ERROR: wrong number of fields in from_csv. got {} but should have 10'.format(len(fields)))
            print(fields)
            return None

        self.user = User.objects.get(username=fields[0])
        self.name = fields[1]
        self.locale = fields[2]
        self.city = fields[3]
        self.outdoor = fields[4] == '1'
        self.dog_fiendly = fields[5] == '1'
        self.rating = fields[6]
        self.want_to_go = fields[7] == '1'
        self.good_for = fields[8]
        self.comment = fields[9]
        self.save()
        return self

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
        s += ')'
        return s

# class Artist(models.Model):
#     name = models.CharField('Artist Name', max_length=100)
#     nickname = models.CharField(max_length=80, blank=True)
#     fuzzy = models.CharField(max_length=100)
#     active = models.BooleanField(default=True, blank=True)
#     want_to_see = models.BooleanField(default=False, blank=True)

#     @classmethod
#     def create_by_name(cls, *args):
#         self = cls()
#         LibStats.add_artist()
#         if len(args) > 0:
#             self.name = clean_name(args[0])
#             self.fuzzy = fuzzify(self.name)
#         else:
#             self.name = ''

#         if len(args) > 1:
#             self.nickname = args[1]
#         else:
#             self.nickname = ''

#         if len(args) > 2:
#             self.active = args[2]
#         else:
#             self.active = True

#         if len(args) > 3:
#             self.want_too_see = args[3]
#         else:
#             self.want_to_see = False

#         self.save()
#         return self

#     @classmethod
#     def get_by_name(cls, artist_name):
#         try:
#             a = cls.objects.get(fuzzy=fuzzify(artist_name))
#         except:
#             a = cls.create_by_name(artist_name)
#         return a

#     @classmethod
#     def get_matching(cls, search_string):
#         return [x for x in cls.objects.all() if x.name.lower().find(search_string) != -1]

#     def set_want_to_see(self):
#         if not self.want_to_see:
#             LibStats().mod_artist()
#             self.want_to_see = True
#             self.save()

#     def __str__(self):
#         return 'Artist:' + self.name

#     class Meta:
#         app_label = 'mdb'

#     def __repr__(self):
#         return "Artist('{}:{}', '{}', {}, {})".format(self.id,
#                                                       self.name,
#                                                       self.nickname,
#                                                       self.active,
#                                                       self.want_to_see)


# class Concert(models.Model):
#     date = models.DateField()
#     artist = models.ManyToManyField(Artist)
#     venue = models.CharField(max_length=30)

#     @classmethod
#     def create(cls, date, venue):
#         self = cls()
#         if isinstance(date, str):
#             if date.find('-') != -1:
#                 date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
#             elif date.find('/') != -1:
#                 date = datetime.datetime.strptime(date, '%m/%d/%Y').date()

#         self.date = date
#         self.venue = venue
#         self.save()
#         return self

#     def add_artist(self, artist):
#         a = Artist.get_by_name(artist)
#         self.artist.add(a)
#         self.save()

#     def add_artists(self, list_of_artists):
#         for a in list_of_artists:
#             self.add_artist(a)

#     def __str__(self):
#         return "ConcertDate('%d-%02d-%02d','%s',%s)" % (self.date.year,
#                                                         self.date.month,
#                                                         self.date.day,
#                                                         self.venue,
#                                                         str(self.artist.all()))

#     def __repr__(self):
#         return "ConcertDate('%d-%02d-%02d','%s',%s)" % (self.date.year,
#                                                         self.date.month,
#                                                         self.date.day,
#                                                         self.venue,
#                                                         str(self.artist.all()))

#     class Meta:
#         app_label = 'mdb'


# class Album(models.Model):
#     name = models.CharField(max_length=100)
#     fuzzy = models.CharField(max_length=100)
#     nickname = models.CharField(max_length=80, blank=True)
#     artist = models.ForeignKey(Artist)

#     @classmethod
#     def create_by_name(cls, album_name, artist_object):
#         self = cls()
#         LibStats().add_album()
#         self.name = clean_name(album_name)
#         self.fuzzy = fuzzify(self.name)
#         self.artist = artist_object
#         self.save()
#         return self

#     @classmethod
#     def get_by_name(cls, album_name, artist):
#         if isinstance(artist, str):
#             # need to lookup artist
#             artist_object = Artist.get_by_name(artist)
#         else:
#             artist_object = artist

#         try:
#             # todo: handle case of multiple albums with same name
#             a = cls.objects.get(fuzzy=fuzzify(album_name))
#         except:
#             a = cls.create_by_name(album_name, artist_object)
#         return a

#     def __str__(self):
#         if self.artist:
#             return '%s (%s)' % (self.name, self.artist.name)
#         else:
#             return '%s (no artist)' % self.name

#     class Meta:
#         app_label = 'mdb'

#     def __repr__(self):
#         return "Album('{}', '{}', {})".format(self.name,
#                                               self.nickname,
#                                               self.artist)


# class NameMap(models.Model):
#     fname = models.CharField(max_length=100)
#     tname = models.CharField(max_length=100)

#     @classmethod
#     def add(cls, from_name, to_name):
#         try:
#             cls.objects.get(fname=from_name)
#         except:
#             m = cls(fname=from_name, tname=to_name)
#             m.save()

#     @classmethod
#     def map(cls, from_name):
#         try:
#             mapping = cls.objects.get(fname=from_name)
#             return mapping.tname
#         except:
#             return False


# class Song(models.Model):
#     genre_list = (
#         ('rock', 'Rock'),
#         ('pop', 'Pop'),
#         ('blues', 'Blues'),
#         ('country', 'Country'),
#         ('jazz', 'Jazz'),
#         ('parody', 'Parody'),
#         ('lossless', 'Lossless')
#     )
#     grouping_list = (
#         ('skating', 'Skating'),
#         ('hifi', 'HiFi'),
#         ('rhythm', 'Rhythm'),
#         ('party', 'Party'),
#         ('lossless', 'Lossless')
#     )
#     name = models.CharField(max_length=100)
#     fuzzy = models.CharField(max_length=100)
#     nickname = models.CharField(max_length=80, blank=True)
#     genre = models.CharField(max_length=20, choices=genre_list)
#     rating = models.IntegerField(default=0)
#     grouping = models.CharField(max_length=20, blank=True, choices=grouping_list)
#     album = models.ForeignKey(Album)
#     taglist = models.CharField(max_length=80, blank=True)

#     @classmethod
#     def create_by_name(cls, name, album, artist):
#         s = cls()
#         LibStats().add_song()
#         if isinstance(album, str):
#             album = Album.get_by_name(album, artist)

#         s.name = clean_name(name)
#         s.fuzzy = fuzzify(s.name)
#         s.album = album
#         s.save()
#         return s

#     @classmethod
#     def get_by_name(cls, name, album, artist):
#         matches = cls.objects.filter(fuzzy=fuzzify(name))
#         # We want to return the best match.  If the song name matches
#         # but the album does not try matching on artist
#         s = [x for x in matches if x.album.fuzzy == fuzzify(album)]
#         if len(s) == 0:
#             s = [x for x in matches if x.album.artist.fuzzy == fuzzify(artist)]
#         if len(s) > 0:
#             if (len(s) == 1):
#                 s = s[0]
#             else:
#                 print('\nWarning: Duplicate songs found (%d):' % len(s))
#                 for x in s:
#                     print('    {}'.format(x))
#                 print()
#                 s = s[0]
#         else:
#             s = cls.create_by_name(name, album, artist)
#         return s

#     @classmethod
#     def find_by_name(cls, name, album, artist):
#         matches = cls.objects.filter(fuzzy=fuzzify(name))
#         # We want to return the best match.  If the song name matches
#         # but the album does not try matching on artist
#         s = [x for x in matches if x.album.fuzzy == fuzzify(album)]
#         if len(s) == 0:
#             s = [x for x in matches if x.album.artist.fuzzy == fuzzify(artist)]
#         if len(s) > 0:
#             if (len(s) > 1):
#                 print('\nWarning: Duplicate songs found (%d):' % len(s))
#                 for x in s:
#                     print('    {}'.format(x))
#                 print()
#                 s = s[0]
#             return s[0]
#         else:
#             return False

#     @classmethod
#     def get_matching(cls, search_string):
#         return [x for x in cls.objects.all() if x.name.lower().find(search_string.lower()) != -1]

#     def set_attr(self, genre, grouping, rating, tags):
#         changed = False
#         if genre and (self.genre != genre):
#             self.genre = genre
#             changed = True

#         if grouping and (self.grouping != grouping):
#             self.grouping = grouping
#             changed = True

#         try:
#             rating = int(rating)
#         except:
#             rating = 0

#         if (rating != 0) and (self.rating != rating):
#             self.rating = rating
#             changed = True

#         start_tags = self.taglist
#         if start_tags and start_tags != '':
#             newtags = tags_to_set(tags)
#             ctags = tags_to_set(start_tags)
#             for x in newtags:
#                 ctags.add(x)
#             newtags = set_to_tags(ctags)
#             if newtags != start_tags:
#                 self.taglist = newtags
#                 changed = True
#         else:
#             if tags != '':
#                 self.taglist = tags
#                 changed = True

#         if changed:
#             LibStats().mod_song()
#             self.save()

#     def get_tags(self):
#         return sorted(tags_to_set(self.taglist))

#     def __str__(self):
#         if self.album:
#             return '%s (%s)' % (self.name, self.album.name)
#         else:
#             return '%s (no album)' % self.name

#     def __repr__(self):
#         return "Song('{}', '{}', '{}',[{}, {}, {}, {}])".format(self.name,
#                                                                 self.album.name,
#                                                                 self.album.artist.name,
#                                                                 self.genre,
#                                                                 self.grouping,
#                                                                 self.rating,
#                                                                 self.taglist)

    class Meta:
        app_label = 'places'
