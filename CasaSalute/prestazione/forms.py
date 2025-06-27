from django import forms
from .models import Prestazione

# Form completo (per segreteria/admin)
class PrestazioneForm(forms.ModelForm):
    class Meta:
        model = Prestazione
        fields = ['tipo', 'paziente', 'ambulatorio', 'infermiere', 'prenotazione', 'data', 'esito', 'note']

# Form usato dal paziente per richiedere
class PrestazioneInfermieristicaForm(forms.ModelForm):
    class Meta:
        model = Prestazione
        fields = ['tipo', 'note']  # Questi due bastano

# Form usato dall'infermiere per aggiungere solo esito
class EsitoPrestazioneForm(forms.ModelForm):
    class Meta:
        model = Prestazione
        fields = ['esito']
