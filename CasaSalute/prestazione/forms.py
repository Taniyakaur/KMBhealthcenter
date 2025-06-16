from django import forms
from .models import Prestazione

class PrestazioneForm(forms.ModelForm):
    class Meta:
        model = Prestazione
        fields = ['tipo', 'paziente', 'ambulatorio', 'infermiere', 'prenotazione', 'data', 'esito', 'note']