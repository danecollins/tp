from django import forms
from .models import Watcher



class WatcherAddForm(forms.ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Watcher
        fields = ['name', 'tag', 'freq']
        widgets = {
            'name': forms.TextInput(attrs={'class': "large"}),
        }


class WatcherEditForm(forms.ModelForm):
    required_css_class = 'required'
    large = forms.TextInput(attrs={'class': "large"})
    class Meta:
        model = Watcher
        fields = ['name', 'tag', 'freq', 'active']
        widgets = {
            'name': forms.TextInput(attrs={'class': "large"}),
        }

