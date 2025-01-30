from django import forms
from .models import Visita

class VisitaForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields = ['paziente', 'medico', 'tipo_visita', 'data', 'ora', 'regime']