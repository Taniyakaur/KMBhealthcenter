from django import forms
from .models import Prestazione

class PrestazioneForm(forms.ModelForm):
    class Meta:
        model = Prestazione
        fields = ['paziente', 'infermiere', 'tipo_prestazione', 'data_prenotazione', 'ora_prenotazione', 'data_prestazione', 'esito', 'note']