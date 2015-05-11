from django.shortcuts import render

# Create your views here.
from models import Vote


def man(request):
    v = Vote(type=False)
    v.save()
    votes = Vote.objects.all()
    mtot = len([x for x in votes if not x.type])
    wtot = len([x for x in votes if x.type])
    return render(request, 'vote/vote.html', {'type': 'man',
                                              'mtot': mtot,
                                              'wtot': wtot})


def woman(request):
    v = Vote(type=True)
    v.save()
    votes = Vote.objects.all()
    mtot = len([x for x in votes if not x.type])
    wtot = len([x for x in votes if x.type])
    return render(request, 'vote/vote.html', {'type': 'woman',
                                              'mtot': mtot,
                                              'wtot': wtot})
