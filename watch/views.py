from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .models import Event, Watcher, id_generator
from .forms import WatcherAddForm, WatcherEditForm
import pdb


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
        form = WatcherAddForm(request.POST)
        if form.is_valid():
            form.save()
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
