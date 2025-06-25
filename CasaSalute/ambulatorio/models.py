from django.db import models

class Ambulatorio(models.Model):
    AMBULATORIO_TIPO = [
        ('visite', 'Ambulatorio Visite'),
        ('prestazioni', 'Ambulatorio Prestazioni'),
    ]
    id = models.BigAutoField(primary_key=True)
    tipo = models.CharField(max_length=20, choices=AMBULATORIO_TIPO)

    def __str__(self):
        return f"{self.get_tipo_display()} (ID: {self.id})"

class AmbulatorioVisite(models.Model):
    ambulatorio = models.OneToOneField(Ambulatorio, on_delete=models.CASCADE)
    VISITE_TIPO = [
        ('adulti', 'Per adulti'),
        ('pediatrico', 'Pediatrico'),
    ]
    sotto_tipo = models.CharField(max_length=20, choices=VISITE_TIPO)

    def __str__(self):
        return f"{self.ambulatorio} - {self.get_sotto_tipo_display()}"

class AmbulatorioPrestazioni(models.Model):
    ambulatorio = models.OneToOneField(Ambulatorio, on_delete=models.CASCADE)
    PRESTAZIONI_TIPO = [
        ('prelievi', 'Sala prelievi'),
        ('medicazioni', 'Sala medicazioni'),
    ]
    sotto_tipo = models.CharField(max_length=20, choices=PRESTAZIONI_TIPO)

    def __str__(self):
        return f"{self.ambulatorio} - {self.get_sotto_tipo_display()}"