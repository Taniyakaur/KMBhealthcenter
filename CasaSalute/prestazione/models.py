from django.db import models
from django.utils.translation import gettext_lazy as _

class TipoPrestazione(models.TextChoices):
    PRELIEVO = 'prelievo', _('Prelievo')
    MEDICAZIONE = 'medicazione', _('Medicazione')

class Prestazione(models.Model):
    tipo = models.CharField(max_length=20, choices=TipoPrestazione.choices)
    paziente = models.ForeignKey('users.Paziente', on_delete=models.CASCADE, related_name="prestazioni")  # relazione con il modello in app users
    infermiere = models.ForeignKey('users.Infermiere', on_delete=models.SET_NULL, null=True, related_name="prestazioni_infermiere") # relazione con il modello in app users
    data = models.DateTimeField()
    esito = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_tipo_display()} per {self.paziente} il {self.data.strftime('%Y-%m-%d %H:%M')}"
