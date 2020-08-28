from django import forms

from .models import Garden, Area, Event


class GardenForm(forms.ModelForm):
    class Meta:
        model = Garden
        fields = [
            'name',
            'city',
        ]


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = [
            'garden',
            'name',
            'irrigation_type'

        ]


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'name',
            'data',
            'type',
        ]
