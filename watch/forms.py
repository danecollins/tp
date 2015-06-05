from django import forms



class WatcherForm(forms.Form):
    required_css_class = 'required'
    large = forms.TextInput(attrs={'class': "large"})

    name = forms.CharField(label='Name', max_length=40, required=True, widget=large)
    tag = forms.CharField(label='Tag', max_length=10)
    freq = forms.IntegerField(label='Frequency in Hours')
