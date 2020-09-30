from django import forms
from .models import Garden, Area, Location, CalendarIrrigation


class GardenForm(forms.ModelForm):
    city = forms.ModelChoiceField(label='Città', queryset=Location.objects.all(), to_field_name="city",
                                  widget=forms.TextInput(attrs={'placeholder':'inserisci il comune'}))
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

class CalendarIrrigationForm(forms.ModelForm):
    class Meta:
        model = CalendarIrrigation
        exclude = ('area',)
