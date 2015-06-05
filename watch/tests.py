from django.test import TestCase

from watch.models import Event, Watcher, id_generator
from django.utils import timezone


class TestEvent(TestCase):
    def test_create_ids(self):
        id1 = id_generator()
        self.assertEqual(len(id1), 8)
        id2 = id_generator()
        self.assertEqual(len(id2), 8)
        self.assertTrue(id1 != id2)

    def test_create(self):
        id1 = id_generator()
        id2 = id_generator()
        x = Event(tag=id1, log_type=Event.LOG,
                  time=timezone.now())
        x.save()
        x = Event(tag=id2, log_type=Event.NOTIFICATION,
                  time=timezone.now())
        x.save()
        events = Event.objects.all()
        self.assertEqual(len(events), 2)
        x = Event.objects.get(tag=id1)
        self.assertEqual(x.log_type, Event.LOG)
        x = Event.objects.get(tag=id2)
        self.assertEqual(x.log_type, Event.NOTIFICATION)


class TestWatcher(TestCase):
    def test_create(self):
        x = Watcher(name='DB backup',
                    tag=id_generator(),
                    freq=60)
        x.save()
        self.assertEqual(len(Watcher.objects.all()), 1)

    def test_string_rep(self):
        x = Watcher(name='db backup', tag='hello', freq=60, active=True)
        x.save()
        expect = "Watcher(db backup,hello,60,True)"
        self.assertEqual(expect, str(x))
        expect = "Watcher(name='db backup', tag='hello', freq=60, active=True)"
        self.assertEqual(expect, x.__repr__())

