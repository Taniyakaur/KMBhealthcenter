from django import forms
from .models import Visita
from .models import PrenotazioneVisita
from users.models import Medico, Paziente
from ambulatorio.models import Ambulatorio
from django.forms.widgets import TimeInput

class VisitaForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields = ['prenotazione', 'ambulatorio', 'esito']  # Usa solo i campi esistenti nel modello Visita

# FORM PER PRENOTAZIONE VISITA 
class PrenotazioneForm(forms.ModelForm):
    class Meta:
        model = PrenotazioneVisita
        fields = ['medico', 'data', 'ora', 'tipo', 'regime']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'ora': TimeInput(format='%H:%M', attrs={'type': 'time'}), 
            'paziente': forms.Select(attrs={'class': 'form-control'}),
            'medico': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'regime': forms.Select(attrs={'class': 'form-control'}),
        }
        

# FORM PER INSERIMENTO ESITO VISITA
class EsitoVisitaForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields = ['esito']
        widgets = {
            'esito': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Inserisci esito visita...'})
        }

