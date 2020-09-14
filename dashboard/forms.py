from django import forms
from .models import Garden, Area


class GardenForm(forms.ModelForm):
    class Meta:
        model = Garden
        fields = [
            'name',
            'city',
            'image',

        ]


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = [
            'name',
            'irrigation_type',
        ]
