from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import time

# MODELLO PRENOTAZIONE VISITA
class PrenotazioneVisita(models.Model):
    TIPO = [
        ('adulti', 'Per adulti'),
        ('pediatrica', 'Pediatrica'),
    ]
    REGIME = [
        ('ordinaria', 'Ordinaria'),
        ('urgente', 'Urgente'),
    ]
    id = models.BigAutoField(primary_key=True)
    paziente = models.ForeignKey("users.Paziente", on_delete=models.CASCADE)
    medico = models.ForeignKey("users.Medico", on_delete=models.CASCADE)
    data = models.DateField()
    ora = models.TimeField()
    tipo = models.CharField(max_length=20, choices=TIPO)
    regime = models.CharField(max_length=20, choices=REGIME)

    def clean(self):
        if self.ora < time(8, 0) or self.ora > time(18, 0):
            raise ValidationError("Le prenotazioni devono essere tra le 08:00 e le 18:00")

    def __str__(self):
        return f"Prenotazione di {self.paziente} con {self.medico} il {self.data} alle {self.ora}"

    class Meta:
        ordering = ['data', 'ora']  # Ordinamento per data e orario
        verbose_name = "Prenotazione visita"
        verbose_name_plural = "Prenotazioni visite"

# MODELLO VISITA
class Visita(models.Model):
    id = models.BigAutoField(primary_key=True)
    prenotazione = models.OneToOneField(PrenotazioneVisita, on_delete=models.CASCADE)
    ambulatorio = models.ForeignKey("ambulatorio.Ambulatorio", on_delete=models.SET_NULL, null=True)
    esito = models.TextField(blank=True, null=True)

    @property
    def medico(self):
        return self.prenotazione.medico

    @property
    def paziente(self):
        return self.prenotazione.paziente

    def __str__(self):
        return f"Visita di {self.paziente} con {self.medico}"

    class Meta:
        verbose_name = "visita"
        verbose_name_plural = "visite"