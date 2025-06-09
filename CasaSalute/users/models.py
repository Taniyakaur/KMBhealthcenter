from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from datetime import time


# MODELLO BASE GENERICO
class UtenteBase(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # collegamento all'account Django
    cognome = models.CharField(max_length=50)
    nome = models.CharField(max_length=50)
    codice_fiscale = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        abstract = True  # questo rende la classe astratta


# MODELLO MEDICO
class Medico(UtenteBase):
    specialita = models.CharField(max_length=100, blank=True, null=True)
    assenze_pianificate = models.JSONField(blank=True, null=True)
    medici_sostituibili = models.ManyToManyField("self", blank=True)
    pazienti_in_cura = models.ForeignKey("Medico", on_delete=models.SET_NULL, null=True, related_name="medico_pazienti_in_cura")

    def disponibilita(self, data):
        if self.assenze_pianificate and data in self.assenze_pianificate:
            return False
        return True

    def __str__(self):
        return f"Dr./Dr.ssa {self.nome} {self.cognome}"


# MODELLO INFERMIERE
class Infermiere(UtenteBase):
   giorni_servizio = models.JSONField(blank=True, null=True) # Es. "Lunedì, Mercoledì, Venerdì"

   def disponibilita(self):
        # Logica per verificare la disponibilità
        pass

   def __str__(self):
        return f"Infermiere {self.nome} {self.cognome}"


# MODELLO PAZIENTE
class Paziente(UtenteBase):
    data_nascita = models.DateField()
    luogo_nascita = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    medico_curante = models.ForeignKey("Medico", on_delete=models.SET_NULL, null=True, related_name="medico_pazienti_curante")
    referente_adulto = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True)  # Per i minori di 14 anni

    def is_minor(self):
        from datetime import date
        today = date.today()
        return (today.year - self.data_nascita.year - ((today.month, today.day) < (self.data_nascita.month, self.data_nascita.day))) < 14

    def __str__(self):
        return f"{self.nome} {self.cognome} - {self.codice_fiscale}"


# MODELLO SEGRETERIA
class Segreteria(UtenteBase):
    ruolo = models.CharField(max_length=100, default='Segreteria')  # Ruolo fisso per la segreteria

    def __str__(self):
        return f"Segretario/a {self.nome} {self.cognome}"


# MODELLO AMBULATORIO
class Ambulatorio(models.Model):
    TIPO = [
        ('adulti', 'Per adulti'),
        ('pediatrico', 'Pediatrico')
    ]
    nome = models.CharField(max_length=50)
    tipo = models.CharField(max_length=20, choices=TIPO)

    def __str__(self):
        return f"{self.nome} ({self.tipo})"