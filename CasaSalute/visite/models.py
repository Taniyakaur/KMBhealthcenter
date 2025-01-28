from django.db import models

class Visita(models.Model):
    TIPO_VISITA_CHOICES = [
        ('curante', 'Medico Curante'),
        ('sostituzione', 'In Sostituzione del Medico Curante'),
        ('urgenza', 'D\'Urgenza'),
    ]

    paziente = models.ForeignKey('users.Paziente', on_delete=models.CASCADE)
    medico = models.ForeignKey('users.Medico', on_delete=models.CASCADE)
    ambulatorio = models.CharField(max_length=255)
    esito = models.TextField()
    data = models.DateField()
    ora = models.TimeField()
    urgenza = models.BooleanField(default=False)
    tipo_visita = models.CharField(max_length=20, choices=TIPO_VISITA_CHOICES)

    def __str__(self):
        return f"Visita di {self.paziente} con {self.medico} il {self.data} alle {self.ora}"
