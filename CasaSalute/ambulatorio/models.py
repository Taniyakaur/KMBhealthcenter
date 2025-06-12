from django.db import models

# MODELLO AMBULATORIO
class Ambulatorio(models.Model):
    TIPO = [
        ('adulti', 'Per adulti'),
        ('pediatrico', 'Pediatrico'),
        ('prelievi', 'Sala prelievi'),
        ('medicazioni', 'Sala medicazioni'),
    ]
    id = models.BigAutoField(primary_key=True)
    tipo = models.CharField(max_length=20, choices=TIPO)

    def __str__(self):
        return f"Ambulatorio {self.id} ({self.get_tipo_display()})"