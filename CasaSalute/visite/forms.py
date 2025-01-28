from django import forms
from .models import Visita

class VisitaForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields = ['paziente', 'medico', 'ambulatorio', 'esito', 'data', 'ora', 'urgenza', 'tipo_visita']