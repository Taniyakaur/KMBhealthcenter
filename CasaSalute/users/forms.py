from django import forms
from .models import Medico, Infermiere, Paziente, Segreteria

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['username', 'password', 'nome', 'cognome', 'specializzazione', 'telefono', 'email']
    
    def save(self, commit=True):                           # override del metodo save
        user = super().save(commit=False)                  # se commit=False non salva l'istanza user
        user.set_password(self.cleaned_data['password'])   # prende password dell'utente
        if commit:
            user.save()
        return user

class InfermiereForm(forms.ModelForm):
    class Meta:
        model = Infermiere
        fields = ['username', 'password', 'nome', 'cognome', 'telefono', 'email']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class PazienteForm(forms.ModelForm):
    class Meta:
        model = Paziente
        fields = ['codice_sanitario', 'username', 'password', 'nome', 'cognome', 'data_di_nascita', 'indirizzo', 'telefono', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class SegreteriaForm(forms.ModelForm):
    class Meta:
        model = Segreteria
        fields = ['username', 'password', 'nome', 'cognome', 'telefono', 'email']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user