from django.db import models
from django.contrib.auth.models import User

# MODELLO MEDICO
class Medico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Collegamento all'account Django
    cognome = models.CharField(max_length=50)
    nome = models.CharField(max_length=50)
    codice_fiscale = models.CharField(max_length=16, unique=True)
    specialita = models.CharField(max_length=100, blank=True, null=True)
    assenze_pianificate = models.TextField(blank=True, null=True)  # Potrebbe essere un JSON con date
    medici_sostituibili = models.ManyToManyField("self", blank=True)

    def __str__(self):
        return f"Dr./Dr.ssa {self.nome} {self.cognome}"

# MODELLO INFERMIERE
class Infermiere(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cognome = models.CharField(max_length=50)
    nome = models.CharField(max_length=50)
    codice_fiscale = models.CharField(max_length=16, unique=True)
    giorni_servizio = models.TextField(blank=True, null=True)  # Es. "Lunedì, Mercoledì, Venerdì"

    def __str__(self):
        return f"Infermiere {self.nome} {self.cognome}"

# MODELLO PAZIENTE
class Paziente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    codice_sanitario = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=50)
    cognome = models.CharField(max_length=50)
    data_nascita = models.DateField()
    luogo_nascita = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    medico_curante = models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True, related_name="pazienti")
    referente_adulto = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True)  # Per i minori di 14 anni

    def __str__(self):
        return f"{self.nome} {self.cognome} - {self.codice_sanitario}"

# MODELLO PRENOTAZIONE VISITA
class Prenotazione(models.Model):
    TIPO_VISITA = [
        ('medico_curante', 'Visita con medico curante'),
        ('sostituto', 'Visita con medico sostituto'),
        ('urgenza', 'Visita d’urgenza')
    ]

    paziente = models.ForeignKey(Paziente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    data = models.DateField()
    orario = models.TimeField()
    tipo = models.CharField(max_length=20, choices=TIPO_VISITA)
    stato = models.CharField(max_length=20, default='Prenotato')

    def __str__(self):
        return f"Prenotazione di {self.paziente} con {self.medico} il {self.data} alle {self.orario}"

# MODELLO VISITA
class Visita(models.Model):
    paziente = models.ForeignKey(Paziente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    data = models.DateField()
    urgenza = models.BooleanField(default=False)
    tipo = models.CharField(max_length=20, choices=Prenotazione.TIPO_VISITA)
    esito = models.TextField()
    personale_infermieristico = models.ForeignKey(Infermiere, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Visita di {self.paziente} con {self.medico} il {self.data}"
