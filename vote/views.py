from django.shortcuts import render
from django.db.models import Count

# Create your views here.
from vote.models import Vote, Survey

Man = False
Woman = True


def index(request):
    s = Survey.get()
    current_vote = request.GET.get('type')
    current_car = request.GET.get('car')
    if current_vote in ('man', 'woman'):
        if current_vote == 'man':
            v = Vote(type=Man)
        else:
            v = Vote(type=Woman)
        v.survey = s
        v.save()
    elif current_car:
        if current_car != 'delete':
            v = Vote()
            v.survey = s
            v.choice = current_car
            v.save()
        else:
            vote = Vote.objects.last()
            vote.delete()

    votes = Vote.objects.filter(survey=s).order_by('-date')
    if s == 'cars16':
        cnt = votes.count()
        tallies = Vote.objects.filter(survey=s).values('choice').annotate(Count('choice')).order_by('choice')
        return render(request, 'vote/cars.html', {'vtot': cnt,
                                                  'tallies': tallies,
                                                  'survey': s,
                                                  'votes': votes[0:5]})
    else:
        mtot = votes.filter(type=Man).count()
        wtot = votes.filter(type=Woman).count()
        return render(request, 'vote/index.html', {'vtot': mtot+wtot,
                                                   'mtot': mtot,
                                                   'wtot': wtot,
                                                   'survey': s,
                                                   'votes': votes[0:5]})


def man(request):
    v = Vote(type=False)
    v.survey = Survey.get()
    v.save()
    votes = Vote.objects.filter(survey=v.survey).order_by('-date')
    mtot = votes.filter(type=Man).count()
    wtot = votes.filter(type=Woman).count()
    return redirect('/vote/')
    # return render(request, 'vote/vote.html', {'type': 'man',
    #                                           'survey': v.survey,
    #                                           'mtot': mtot,
    #                                           'wtot': wtot,
    #                                           'votes': votes[0:5]})


def woman(request):
    v = Vote(type=True)
    v.survey = Survey.get()
    v.save()
    votes = Vote.objects.filter(survey=v.survey).order_by('-date')
    mtot = votes.filter(type=Man).count()
    wtot = votes.filter(type=Woman).count()
    return redirect('/vote/')
    # return render(request, 'vote/vote.html', {'type': 'woman',
    #                                           'survey': v.survey,
    #                                           'mtot': mtot,
    #                                           'wtot': wtot,
    #                                           'votes': votes[0:5]})


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
