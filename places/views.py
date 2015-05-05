from django.shortcuts import render
from places.models import Place

# Create your views here.


def index(request):
    return render(request, 'places/index.html')
