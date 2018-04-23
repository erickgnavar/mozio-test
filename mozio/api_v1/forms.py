from django import forms


class ServiceAreaForm(forms.Form):

    lat = forms.FloatField()
    lng = forms.FloatField()
