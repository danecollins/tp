from django import forms
from .models import VisitType

rating_choices = ((0, 'Not Rated'), (1, '1 Star - OK'),
                  (2, '2 Stars - Really Good'), (3, '3 Stars - A Favorite'))

cuisine_choices = (('American', 'American'),
                   ('BBQ', 'BBQ'),
                   ('Cuban', 'Cuban'),
                   ('Chinese', 'Chinese'),
                   ('French', 'French'),
                   ('Greek', 'Greek'),
                   ('Indian', 'Indian'),
                   ('Italian', 'Italian'),
                   ('Japanese', 'Japanese'),
                   ('Korean', 'Korean'),
                   ('Mediterranean', 'Mediterranean'),
                   ('Mexican', 'Mexican'),
                   ('Pizza', 'Pizza'),
                   ('Thai', 'Thai'),
                   ('Other', 'Other'))


class PlaceForm(forms.Form):
    required_css_class = 'required'
    large = forms.TextInput(attrs={'class': "large"})

    name = forms.CharField(label='Name', max_length=100, required=True, widget=large)
    city = forms.CharField(label='City', max_length=100)
    locale = forms.CharField(label='Locale', max_length=40)
    cuisine = forms.ChoiceField(label='Cuisine', choices=cuisine_choices, required=False)
    outdoor = forms.BooleanField(label='Ourdoor Seating', required=False)
    dog_friendly = forms.BooleanField(label='Dog Friendly', required=False)
    visited = forms.TypedChoiceField(label='Visit Type',
                                     choices=VisitType.type_list(), coerce=int)
    rating = forms.TypedChoiceField(label='Rating',
                                    choices=rating_choices, coerce=int)
    good_for = forms.CharField(label='Good For', max_length=50, required=False)
    comment = forms.CharField(label='Comment', max_length=200, required=False, widget=large)
    yelp = forms.URLField(label='Yelp URL', max_length=200, required=False, widget=large)
