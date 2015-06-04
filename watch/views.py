from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .models import Event, Watcher
from .forms import WatcherForm


def event_history(request):
    event_list = Event.objects.all()
    if len(event_list) > 30:
        event_list = event_list[:-30]
    return render(request, 'watch/events.html',
                  {'event_list': event_list})


def list(request):
    watcher_list = Watcher.objects.all()
    return render(request, 'watch/list.html',
                  {'wl': watcher_list})


def add(request):
    form = WatcherForm(request.POST or None)
    if form.is_valid():
        watch = form.save(commit=False)
        watch.save()
        return redirect('/watch/list')
    return render(request, 'watch/add.html', {'form': form})


def details(request, id):
    watcher = get_object_or_404(Watcher, id=id)
    return render(request, 'watch/details.html',
                  {'watcher': watcher})
