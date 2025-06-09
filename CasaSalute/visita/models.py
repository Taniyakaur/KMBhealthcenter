from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import time

# MODELLO PRENOTAZIONE VISITA
class Prenotazione(models.Model):
    TIPO_VISITA = [
        ('medico_curante', 'Visita con medico curante'),
        ('sostituto', 'Visita con medico sostituto'),
        ('urgenza', 'Visita d’urgenza')
    ]

    paziente = models.ForeignKey("users.Paziente", on_delete=models.CASCADE)
    medico = models.ForeignKey("users.Medico", on_delete=models.CASCADE)
    data = models.DateField()
    orario = models.TimeField()
    tipo = models.CharField(max_length=20, choices=TIPO_VISITA)
    stato = models.CharField(max_length=20, default='Prenotato')
    ambulatorio = models.ForeignKey("users.Ambulatorio", on_delete=models.SET_NULL, null=True)

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