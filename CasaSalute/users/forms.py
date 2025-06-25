from django import forms
from .models import Medico, Infermiere, AssenzaPianificata
from django.contrib.auth.forms import AuthenticationForm
from .models import PrestazioneInfermieristica

# FORM PER LOGIN
class LoginForm(forms.Form):
    USER_TYPE_CHOICES = [
        ('medico', 'Medico'), 
        ('infermiere', 'Infermiere'),
        ('paziente', 'Paziente'),
        ('segreteria', 'Segreteria')
    ]

    username = forms.CharField(label="Username", max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    user_type = forms.ChoiceField(label="Tipo di utente", choices=USER_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    

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

# FORM PER PRESTAZIONE INFERMIERISTICA
class PrestazioneInfermieristicaForm(forms.ModelForm):
    class Meta:
        model = PrestazioneInfermieristica
        fields = ['paziente', 'tipo', 'data', 'esito', 'note']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'esito': forms.Textarea(attrs={'rows': 3}),
            'note': forms.Textarea(attrs={'rows': 2}),
        }