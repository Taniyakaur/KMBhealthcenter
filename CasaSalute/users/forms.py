from django import forms
from .models import Medico, Infermiere, Prenotazione

# FORM PER MODIFICA DATI MEDICO
class ModificaMedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['cognome', 'nome', 'codice_fiscale', 'specialita', 'assenze_pianificate']

# FORM PER MODIFICA DATI INFERMIERE
class ModificaInfermiereForm(forms.ModelForm):
    class Meta:
        model = Infermiere
        fields = ['cognome', 'nome', 'codice_fiscale', 'giorni_servizio']

# FORM PER PRENOTAZIONE VISITA
class PrenotazioneForm(forms.ModelForm):
    class Meta:
        model = Prenotazione
        fields = ['medico', 'data', 'orario', 'tipo']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'orario': forms.TimeInput(attrs={'type': 'time'})
        }
