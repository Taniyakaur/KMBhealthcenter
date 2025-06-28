from django import forms
from .models import Prestazione, PrenotazionePrestazione
from django.forms.widgets import TimeInput

# form completo (per segreteria/admin)
class PrestazioneForm(forms.ModelForm):
    class Meta:
        model = Prestazione
        fields = ['tipo', 'paziente', 'ambulatorio', 'infermiere', 'prenotazione', 'data', 'esito', 'note']

# form usato dal paziente per richiedere una prestazione
class PrestazioneInfermieristicaForm(forms.ModelForm):
    class Meta:
        model = PrenotazionePrestazione
        fields = ['data', 'orario', 'tipo']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'ora': TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
        }

# form usato dall'infermiere per aggiungere solo esito
class EsitoPrestazioneForm(forms.ModelForm):
    class Meta:
        model = Prestazione
        fields = ['esito']
