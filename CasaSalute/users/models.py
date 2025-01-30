from django.db import models
from django.utils import timezone


class Paziente(models.Model):
    codice_sanitario = models.CharField(max_length=20, unique=True)  # Unique health code
    username = models.CharField(max_length=150, unique=True, primary_key=True)
    password = models.CharField(max_length=128)  # Use CharField for storing hashed passwords
    nome = models.CharField(max_length=255)
    cognome = models.CharField(max_length=255)
    data_di_nascita = models.DateField(null=True, blank=True)
    indirizzo = models.TextField(null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"{self.nome} {self.cognome}"


class Infermiere(models.Model):
    username = models.CharField(max_length=150, unique=True, primary_key=True)
    password = models.CharField(max_length=128)  # Use CharField for storing hashed passwords
    nome = models.CharField(max_length=255)
    cognome = models.CharField(max_length=255)
    data_di_nascita = models.DateField(null=True, blank=True)
    indirizzo = models.TextField(null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    reparto = models.CharField(max_length=255, null=True, blank=True)
    giorni_sala_prelievi = models.CharField(max_length=255, null=True, blank=True)  # Days in blood collection room
    giorni_sala_medicazioni = models.CharField(max_length=255, null=True, blank=True)  # Days in dressing room

    def __str__(self):
        return f"{self.nome} {self.cognome}"


class Medico(models.Model):
    username = models.CharField(max_length=150, unique=True, primary_key=True)
    password = models.CharField(max_length=128)  # Use CharField for storing hashed passwords
    nome = models.CharField(max_length=255)
    cognome = models.CharField(max_length=255)
    data_di_nascita = models.DateField(null=True, blank=True, default=timezone.now)
    specializzazione = models.CharField(max_length=255, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    pazienti_convenzionati = models.ManyToManyField('Paziente', related_name='medici_convenzionati', blank=True)  # Patients associated with the doctor
    medici_sostituibili = models.ManyToManyField('self', symmetrical=False, related_name='medici_sostituti', blank=True)  # Doctors that can be replaced

    def __str__(self):
        return f"{self.nome} {self.cognome}"


class Segreteria(models.Model):
    username = models.CharField(max_length=150, unique=True, primary_key=True)
    password = models.CharField(max_length=128)  # Use CharField for storing hashed passwords
    nome = models.CharField(max_length=255)
    cognome = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"{self.nome} {self.cognome}"
