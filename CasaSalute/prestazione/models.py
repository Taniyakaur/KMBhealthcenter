from django.db import models
from django.utils.translation import gettext_lazy as _


class TipoPrestazione(models.TextChoices):
    PRELIEVO = 'prelievo', _('Prelievo')
    MEDICAZIONE = 'medicazione', _('Medicazione')

class PrenotazionePrestazione(models.Model):
    id = models.BigAutoField(primary_key=True)
    paziente = models.ForeignKey('users.Paziente', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TipoPrestazione.choices)
    data = models.DateField()
    orario = models.TimeField()
    def __str__(self):
        return f"{self.get_tipo_display()} per {self.paziente} il {self.data} alle {self.orario}"
    class Meta:
        verbose_name = "prenotazione prestazione"
        verbose_name_plural = "prenotazioni prestazioni"
        ordering = ['data', 'orario']

class Prestazione(models.Model):
    id = models.BigAutoField(primary_key=True)  
    tipo = models.CharField(max_length=20, choices=TipoPrestazione.choices)
    paziente = models.ForeignKey('users.Paziente', on_delete=models.CASCADE, related_name="prestazioni")  # relazione con il modello in app users
    ambulatorio = models.ForeignKey('ambulatorio.Ambulatorio', on_delete=models.SET_NULL, null=True)  # relazione con il modello ambulatorio
    infermiere = models.ForeignKey('users.Infermiere', on_delete=models.SET_NULL, null=True, related_name="prestazioni_infermiere") # relazione con il modello in app users
    prenotazione = models.OneToOneField('PrenotazionePrestazione', on_delete=models.CASCADE, null=True, blank=True)
    data = models.DateTimeField()
    esito = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_tipo_display()} per {self.paziente} il {self.data.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = "prestazione"
        verbose_name_plural = "prestazioni"
        ordering = ['data']  # Ordinamento per data della prestazione


