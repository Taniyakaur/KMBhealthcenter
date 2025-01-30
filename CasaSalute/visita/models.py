from django.db import models
from django.utils import timezone

class Visita(models.Model):
    TIPO_VISITA_CHOICES = [
        ('pediatrica', 'Pediatrica'),
        ('adulti', 'Per Adulti'),
    ]
    REGIME_VISITA_CHOICES = [
        ('ordinaria', 'Ordinaria'),
        ('urgente', 'Urgente'),
    ]

    paziente = models.ForeignKey('users.Paziente', on_delete=models.CASCADE)
    medico = models.ForeignKey('users.Medico', on_delete=models.CASCADE)
    tipo_visita = models.CharField(max_length=20, choices=TIPO_VISITA_CHOICES)
    data = models.DateField(default=timezone.now)
    ora = models.TimeField()
    regime = models.CharField(max_length=20, choices=REGIME_VISITA_CHOICES, default='ordinaria')
    esito = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Visita di {self.paziente} con {self.medico} il {self.data} alle {self.ora}"
