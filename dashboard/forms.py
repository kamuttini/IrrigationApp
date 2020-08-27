from django import forms

from .models import Garden, Area

class GardenForm(forms.ModelForm):
    class Meta:
        model = Garden
        fields = [
            'name',
            'city'
        ]


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = [
            'garden',
            'name',

        ]

