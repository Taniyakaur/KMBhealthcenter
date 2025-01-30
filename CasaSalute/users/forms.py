from django import forms
from .models import Medico, Infermiere, Paziente, Segreteria

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['username', 'password', 'nome', 'cognome', 'specializzazione', 'telefono', 'email']

class InfermiereForm(forms.ModelForm):
    class Meta:
        model = Infermiere
        fields = ['username', 'password', 'nome', 'cognome', 'telefono', 'email']

class PazienteForm(forms.ModelForm):
    class Meta:
        model = Paziente
        fields = ['codice_sanitario', 'username', 'password', 'nome', 'cognome', 'data_di_nascita', 'indirizzo', 'telefono', 'email']

class SegreteriaForm(forms.ModelForm):
    class Meta:
        model = Segreteria
        fields = ['username', 'password', 'nome', 'cognome', 'telefono', 'email']