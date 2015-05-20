from django.shortcuts import render

# Create your views here.
from models import Vote, Problem


def index(request):
    votes = Vote.objects.all()
    mtot = len([x for x in votes if not x.type])
    wtot = len([x for x in votes if x.type])
    return render(request, 'vote/index.html', {'mtot': mtot,
                                               'wtot': wtot})


def man(request):
    v = Vote(type=False)
    v.problem = Problem.get()
    v.save()
    votes = Vote.objects.all()
    mtot = len([x for x in votes if not x.type])
    wtot = len([x for x in votes if x.type])
    return render(request, 'vote/vote.html', {'type': 'man',
                                              'problem': v.problem,
                                              'mtot': mtot,
                                              'wtot': wtot})


def woman(request):
    v = Vote(type=True)
    v.problem = Problem.get()
    v.save()
    votes = Vote.objects.all()
    mtot = len([x for x in votes if not x.type])
    wtot = len([x for x in votes if x.type])
    return render(request, 'vote/vote.html', {'type': 'woman',
                                              'problem': v.problem,
                                              'mtot': mtot,
                                              'wtot': wtot})


def view_problem(request):
    p = Problem.objects.get(id=1)
    return render(request, 'vote/problem.html', {'p': p})


def set_problem(request, problem):
    try:
        p = Problem.objects.get(id=1)
    except:
        p = Problem()

    p.last = problem
    p.save()
    return view_problem(request)
