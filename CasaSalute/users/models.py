from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from datetime import time


# MODELLO BASE GENERICO
class UtenteBase(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Collegamento all'account Django
    cognome = models.CharField(max_length=50)
    nome = models.CharField(max_length=50)
    codice_fiscale = models.CharField(max_length=16, unique=True)

    class Meta:
        abstract = True  # Questo rende la classe astratta


# MODELLO MEDICO
class Medico(UtenteBase):
    specialita = models.CharField(max_length=100, blank=True, null=True)
    assenze_pianificate = models.JSONField(blank=True, null=True)
    medici_sostituibili = models.ManyToManyField("self", blank=True, related_name="sostituiti_da")
    def disponibilita(self, data):
     if self.assenze_pianificate:
        return str(data) not in self.assenze_pianificate
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
    codice_sanitario = models.CharField(max_length=20, unique=True)
    data_nascita = models.DateField()
    luogo_nascita = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    medico_curante = models.ForeignKey("Medico", on_delete=models.SET_NULL, null=True, related_name="pazienti")
    referente_adulto = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True)  # Per i minori di 14 anni

    def is_minor(self):
        from datetime import date
        today = date.today()
        return (today.year - self.data_nascita.year - ((today.month, today.day) < (self.data_nascita.month, self.data_nascita.day))) < 14

    def __str__(self):
        return f"{self.nome} {self.cognome} - {self.codice_sanitario}"


# MODELLO SEGRETERIA
class Segreteria(UtenteBase):
    ruolo = models.CharField(max_length=100, default='Segreteria')  # Ruolo fisso per la segreteria
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

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


# MODELLO PRENOTAZIONE VISITA
class Prenotazione(models.Model):
    TIPO_VISITA = [
        ('medico_curante', 'Visita con medico curante'),
        ('sostituto', 'Visita con medico sostituto'),
        ('urgenza', 'Visita d’urgenza')
    ]

    paziente = models.ForeignKey("Paziente", on_delete=models.CASCADE)
    medico = models.ForeignKey("Medico", on_delete=models.CASCADE)
    data = models.DateField()
    orario = models.TimeField()
    tipo = models.CharField(max_length=20, choices=TIPO_VISITA)
    stato = models.CharField(max_length=20, default='Prenotato')
    ambulatorio = models.ForeignKey(Ambulatorio, on_delete=models.SET_NULL, null=True)

    def clean(self):
        # Validazione sull'orario
        if self.orario < time(8, 0) or self.orario > time(18, 0):
            raise ValidationError("Le prenotazioni devono essere tra le 08:00 e le 18:00")

    def __str__(self):
        return f"Prenotazione di {self.paziente} con {self.medico} il {self.data} alle {self.orario}"
    class Meta:
        ordering = ['data', 'orario']  # Ordinamento per data e orario


# MODELLO VISITA
class Visita(models.Model):
    prenotazione = models.OneToOneField(Prenotazione, on_delete=models.CASCADE)
    esito = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Visita di {self.prenotazione.paziente} con {self.prenotazione.medico}"


class TipoPrestazione(models.TextChoices):
    PRELIEVO = 'prelievo', _('Prelievo')
    MEDICAZIONE = 'medicazione', _('Medicazione')

class Prestazione(models.Model):
    tipo = models.CharField(max_length=20, choices=TipoPrestazione.choices)
    paziente = models.ForeignKey("Paziente", on_delete=models.CASCADE)
    infermiere = models.ForeignKey("Infermiere", on_delete=models.SET_NULL, null=True)
    data = models.DateTimeField()
    esito = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_tipo_display()} per {self.paziente} il {self.data.strftime('%Y-%m-%d %H:%M')}"
