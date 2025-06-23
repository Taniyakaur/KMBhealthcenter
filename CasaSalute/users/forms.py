from django import forms
from .models import Medico, Infermiere, AssenzaPianificata
from django.contrib.auth.forms import AuthenticationForm

# FORM PER LOGIN
class LoginForm(AuthenticationForm):
    USER_TYPE_CHOICES = [
        ('medico', 'Medico'),
        ('infermiere', 'Infermiere'),
        ('paziente', 'Paziente'),
        ('segreteria', 'Segreteria')
    ]
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        initial='paziente',          #tipo di utente di default
        widget=forms.Select(attrs={'class': 'form-control'})
    )

# FORM PER MODIFICA DATI MEDICO
class ModificaMedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['cognome', 'nome', 'codice_fiscale', 'specializzazione', 'medici_sostituibili']

# FORM PER MODIFICA DATI INFERMIERE
class ModificaInfermiereForm(forms.ModelForm):
    class Meta:
        model = Infermiere
        fields = ['cognome', 'nome', 'codice_fiscale']


# FORM PER ASSENZA PIANIFICATA
class AssenzaPianificataForm(forms.ModelForm):
    class Meta:
        model = AssenzaPianificata
        fields = '__all__'
