from django import forms
from .models import *


class GardenForm(forms.ModelForm):
    city = forms.ModelChoiceField(label='Città', queryset=Location.objects.all(), to_field_name="city",
                                  widget=forms.TextInput(attrs={'placeholder': 'inserisci il comune'}))
    class Meta:
        model = Garden
        fields = [
            'name',
            'image',
            'city'
        ]
        labels= {
            'name': 'Nome',
            'image': 'Immagine'
        }


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = [
            'name',
            'irrigation_type',
        ]
        labels = {
            'name': 'Nome',
            'irrigation_type': 'Tipo di irrigazione'
        }


HOUR_CHOICES = [(datetime.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]

class CalendarIrrigationForm(forms.ModelForm):
    class Meta:
        model = ScheduledIrrigation
        exclude = ('area',)
        widgets = {'hour': forms.Select(choices=HOUR_CHOICES)}


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Setting
        exclude = ('user',)
