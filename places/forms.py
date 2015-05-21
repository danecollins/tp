from django import forms
from .models import VisitType


class PlaceForm(forms.Form):
    required_css_class = 'required'
    large = forms.TextInput(attrs={'class': "large"})

    name = forms.CharField(label='Name', max_length=100, required=True, widget=large)
    city = forms.CharField(label='City', max_length=100)
    locale = forms.CharField(label='Locale', max_length=40)
    cuisine = forms.CharField(label='Cuisine', max_length=40, required=False)
    outdoor = forms.BooleanField(label='Ourdoor Seating', required=False)
    dog_friendly = forms.BooleanField(label='Dog Friendly', required=False)
    visited = forms.TypedChoiceField(label='Visit Type',
                                     choices=VisitType.type_list(), coerce=int)
    rating = forms.IntegerField(label='Rating', min_value=0, max_value=3)
    good_for = forms.CharField(label='Good For', max_length=50, required=False)
    comment = forms.CharField(label='Comment', max_length=200, required=False, widget=large)
    yelp = forms.URLField(label='Yelp URL', max_length=200, required=False, widget=large)
    opentable = forms.URLField(label='Open Table URL', max_length=200, required=False, widget=large)
