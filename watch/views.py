from __future__ import print_function
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .models import Event, Watcher, id_generator
from .forms import WatcherAddForm, WatcherEditForm
from django.utils import timezone
import sys


def event_history(request):
    event_list = Event.objects.all()
    if len(event_list) > 30:
        event_list = event_list[:-30]
    return render(request, 'watch/events.html',
                  {'event_list': event_list})


def list(request):
    watcher_list = Watcher.objects.all()
    return render(request, 'watch/list.html', {'wl': watcher_list})


def add(request):
    if request.method == 'POST':
        watcher = Watcher.objects.get(id=id)
        form = WatcherAddForm(request.POST, instance=watcher)
        if form.is_valid():
            watcher = form.save(commit=False)
            watcher.save()
            return redirect('/watch/list/')
    else:
        form = WatcherAddForm(initial={'tag': id_generator()})
        return render(request, 'watch/add.html', {'form': form})

def edit(request, id):
    if request.method == 'POST':
        form = WatcherEditForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/watch/list/')
    else:
        watcher = Watcher.objects.get(id=id)
        form = WatcherEditForm(instance=watcher)
        return render(request, 'watch/edit.html', {'form': form, 'id': id})


def detail(request, id):
    watcher = get_object_or_404(Watcher, id=id)
    event_list = Event.objects.filter(tag=watcher.tag)
    return render(request, 'watch/details.html',
                  {'watcher': watcher, 'event_list': event_list})


def checkin(request, tag):
    e = Event(tag=tag, log_type=Event.LOG, time=timezone.now())
    e.save()
    return render(request, 'watch/checkin.html',
                  {'tag': tag})

