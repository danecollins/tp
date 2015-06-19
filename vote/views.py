from django.shortcuts import render

# Create your views here.
from vote.models import Vote, Survey


def index(request):
    s = Survey.get()
    votes = Vote.objects.filter(survey=s)
    mtot = len([x for x in votes if not x.type])
    wtot = len([x for x in votes if x.type])
    return render(request, 'vote/index.html', {'mtot': mtot,
                                               'wtot': wtot,
                                               'survey': s})


def man(request):
    v = Vote(type=False)
    v.survey = Survey.get()
    v.save()
    votes = Vote.objects.filter(survey=v.survey)
    mtot = len([x for x in votes if not x.type])
    wtot = len([x for x in votes if x.type])
    return render(request, 'vote/vote.html', {'type': 'man',
                                              'survey': v.survey,
                                              'mtot': mtot,
                                              'wtot': wtot})


def woman(request):
    v = Vote(type=True)
    v.survey = Survey.get()
    v.save()
    votes = Vote.objects.filter(survey=v.survey)
    mtot = len([x for x in votes if not x.type])
    wtot = len([x for x in votes if x.type])
    return render(request, 'vote/vote.html', {'type': 'woman',
                                              'survey': v.survey,
                                              'mtot': mtot,
                                              'wtot': wtot})


def view_survey(request):
    p = Survey.objects.get(id=1)
    return render(request, 'vote/survey.html', {'p': p})


def set_survey(request, name):
    try:
        p = Survey.objects.get(id=1)
    except:
        p = Survey()

    p.last = name
    p.save()
    return view_survey(request)
