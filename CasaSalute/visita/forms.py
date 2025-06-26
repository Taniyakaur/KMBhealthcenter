from django import forms
from .models import Visita
from .models import PrenotazioneVisita
from users.models import Medico, Paziente
from ambulatorio.models import Ambulatorio
from .utils import get_slots
from datetime import timedelta

class VisitaForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields = ['prenotazione', 'ambulatorio', 'esito']  # Usa solo i campi esistenti nel modello Visita

# FORM PER PRENOTAZIONE VISITA

class PrenotazioneForm(forms.ModelForm):
    class Meta:
        model = PrenotazioneVisita
        fields = ['paziente', 'medico', 'data', 'ora', 'tipo', 'regime']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'ora': forms.Select(),  # Cambia in Select per mostrare solo gli slot disponibili
            'paziente': forms.Select(attrs={'class': 'form-control'}),
            'medico': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'regime': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        data = self.initial.get('data') or self.data.get('data')
        medico = self.initial.get('medico') or self.data.get('medico')
        if data and medico:
            from .models import PrenotazioneVisita
            prenotazioni = PrenotazioneVisita.objects.filter(data=data, medico=medico)
            slot_duration = timedelta(minutes=30)
            slots = get_slots(data, slot_duration, prenotazioni)
            self.fields['ora'].choices = [(s, s.strftime("%H:%M")) for s in slots]
        else:
            self.fields['ora'].choices = []

# FORM PER INSERIMENTO ESITO VISITA
class EsitoVisitaForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields = ['esito']
        widgets = {
            'esito': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Inserisci esito visita...'})
        }

