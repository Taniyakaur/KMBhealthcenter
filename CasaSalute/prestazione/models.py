from django.db import models
from django.utils import timezone

class Prestazione(models.Model):
    TIPO_PRESTAZIONE_CHOICES = [
        ('prelievo', 'Prelievo'),
        ('medicazione', 'Medicazione'),
    ]

    paziente = models.ForeignKey('users.Paziente', on_delete=models.CASCADE)
    infermiere = models.ForeignKey('users.Infermiere', on_delete=models.CASCADE)
    tipo_prestazione = models.CharField(max_length=20, choices=TIPO_PRESTAZIONE_CHOICES)
    data_prenotazione = models.DateField(default=timezone.now)
    ora_prenotazione = models.TimeField()
    data_prestazione = models.DateField(null=True, blank=True, default=timezone.now)
    esito = models.TextField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.tipo_prestazione} di {self.paziente} con {self.infermiere} il {self.data_prenotazione} alle {self.ora_prenotazione}"
