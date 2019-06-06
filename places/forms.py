from django import forms
from .models import VisitType

rating_choices = ((0, 'Not Rated'), (1, '1 Star - OK'),
                  (2, '2 Stars - Really Good'), (3, '3 Stars - A Favorite'))

cuisine_choices = (('American', 'American'),
                   ('Bar and Grill', 'Bar and Grill'),
                   ('Brewery', 'Brewery'),
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
                   ('Seafood', 'Seafood'),
                   ('Thai', 'Thai'),
                   ('Other', 'Other'))


class PlaceForm(forms.Form):
    required_css_class = 'required'
    large = forms.TextInput(attrs={'class': "large"})

    name = forms.CharField(label='Name', max_length=100, required=True, widget=large)
    city = forms.CharField(label='City', max_length=100)
    locale = forms.CharField(label='Neighborhood', max_length=40)
    dog_friendly = forms.BooleanField(label='Dog Friendly', required=False)
    visited = forms.TypedChoiceField(label='Visit Type',
                                     choices=VisitType.type_list(), coerce=int)
    rating = forms.TypedChoiceField(label='Rating',
                                    choices=rating_choices, coerce=int)
    good_for = forms.CharField(label='Good For', max_length=50, required=False)
    comment = forms.CharField(label='Comment', max_length=200, required=False, widget=large)


class RestaurantForm(PlaceForm):
    large = forms.TextInput(attrs={'class': "large"})
    cuisine = forms.ChoiceField(label='Cuisine', choices=cuisine_choices, required=False)
    outdoor = forms.BooleanField(label='Outdoor Seating', required=False)
    yelp = forms.URLField(label='Yelp URL', max_length=200, required=False, widget=large)


class HotelForm(PlaceForm):
    large = forms.TextInput(attrs={'class': "large"})
    has_bar = forms.BooleanField(label='Has a bar', required=False)
    tripadvisor = forms.URLField(label='Trip Advisor URL', max_length=200, required=False, widget=large)


class ShareForm(forms.Form):
    from_number = forms.CharField(label='Your Phone # (numbers only)', max_length=20, required=True)
    to_number = forms.CharField(label='Send to Phone # (numbers only)', max_length=20, required=True)
