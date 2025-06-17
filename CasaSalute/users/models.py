from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from datetime import time


# MODELLO BASE GENERICO
class UtenteBase(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)  # collegamento all'account Django
    cognome = models.CharField(max_length=50)
    nome = models.CharField(max_length=50)
    codice_fiscale = models.CharField(max_length=16)

    class Meta:
        abstract = True  # questo rende la classe astratta


# MODELLO MEDICO
class Medico(UtenteBase):
    specialita = models.CharField(max_length=100, blank=True, null=True)
    assenze_pianificate = models.JSONField(blank=True, null=True)
    medici_sostituibili = models.ManyToManyField("self", blank=True)

    class Meta:
        verbose_name = "medico"
        verbose_name_plural = "medici"


# MODELLO INFERMIERE
class Infermiere(UtenteBase):
    giorni_servizio = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Infermiere {self.nome} {self.cognome}"

    class Meta:
        verbose_name = "infermiere"
        verbose_name_plural = "infermieri"


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

    class Meta:
        verbose_name = "paziente"
        verbose_name_plural = "pazienti"


# MODELLO SEGRETERIA
class Segreteria(UtenteBase):
    ruolo = models.CharField(max_length=100, default='Segreteria')  # Ruolo fisso per la segreteria

    def __str__(self):
        return f"Segretario/a {self.nome} {self.cognome}"

    class Meta:
        verbose_name = "segreteria"
        verbose_name_plural = "segreterie"