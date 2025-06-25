from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from datetime import time


# MODELLO BASE GENERICO
class UtenteBase(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)  # collegamento all'account Django
    cognome = models.CharField(max_length=50)
    nome = models.CharField(max_length=50)
    codice_fiscale = models.CharField(max_length=16)

    class Meta:
        abstract = True  # questo rende la classe astratta


# MODELLO USER PROFILE
class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('medico', 'Medico'),
        ('infermiere', 'Infermiere'),
        ('paziente', 'Paziente'),
        ('segreteria', 'Segreteria'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_utente = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return self.user.username

# MODELLO MEDICO

SPECIALIZZAZIONE_CHOICES = [
    ('medicina_generale', 'Medicina Generale'),
    ('pediatria', 'Pediatria'),
    ('cardiologia', 'Cardiologia'),
    ('neurologia', 'Neurologia'),
]
class Medico(UtenteBase):
    specializzazione = models.CharField(max_length=30,   choices=SPECIALIZZAZIONE_CHOICES, blank=True, null=True)
    medici_sostituibili = models.ManyToManyField("self", blank=True)

    def __str__(self):
            return self.user.username

    class Meta:
        verbose_name = "medico"
        verbose_name_plural = "medici"


# MODELLO ASSENZA PIANIFICATA
class AssenzaPianificata(models.Model):
    medico = models.ForeignKey('Medico', on_delete=models.CASCADE, related_name='assenze_pianificate')
    data_inizio = models.DateField()
    data_fine = models.DateField()
    motivo = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.medico} assente dal {self.data_inizio} al {self.data_fine}"
    class Meta:
        verbose_name = "Assenza Pianificata"
        verbose_name_plural = "Assenze Pianificate"


# MODELLO INFERMIERE
class Infermiere(UtenteBase):
    pass  # Non ha campi aggiuntivi rispetto a UtenteBase, ma può essere esteso in futuro

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Infermiere"
        verbose_name_plural = "Infermieri"

class GiornoServizio(models.Model):
    infermiere = models.ForeignKey('Infermiere', on_delete=models.CASCADE, related_name='giorni_servizio')
    giorno = models.CharField(max_length=10, choices=[
        ('lun', 'Lunedì'),
        ('mar', 'Martedì'),
        ('mer', 'Mercoledì'),
        ('gio', 'Giovedì'),
        ('ven', 'Venerdì'),
        ('sab', 'Sabato'),
        ('dom', 'Domenica'),
    ])
    orario_inizio = models.TimeField()
    orario_fine = models.TimeField()

    def __str__(self):
        return f"{self.infermiere} - {self.get_giorno_display()} {self.orario_inizio}-{self.orario_fine}"

    class Meta:
        verbose_name = "giorno di servizio"
        verbose_name_plural = "giorni di servizio"


# MODELLO PAZIENTE
class Paziente(UtenteBase):
    data_nascita = models.DateField()
    luogo_nascita = models.CharField(max_length=100)
    email = models.EmailField(default="insericiEmail@example.com")  # obbligatorio
    medico_curante = models.ForeignKey("Medico", on_delete=models.SET_NULL, null=True, related_name="medico_pazienti_curante")
    referente_adulto = models.CharField(max_length=100, blank=True, null=True, help_text="Nome e cognome del referente adulto per i minori")

    def is_minor(self):
        from datetime import date
        today = date.today()
        return (today.year - self.data_nascita.year - ((today.month, today.day) < (self.data_nascita.month, self.data_nascita.day))) < 18

    def clean(self):
        super().clean()
        if self.is_minor() and not self.referente_adulto:
            from django.core.exceptions import ValidationError
            raise ValidationError({'referente_adulto': 'Il referente adulto è obbligatorio per i minori di 18 anni.'})

    def __str__(self):
        return f"{self.nome} {self.cognome} - {self.codice_fiscale}"

    class Meta:
        verbose_name = "paziente"
        verbose_name_plural = "pazienti"


# MODELLO SEGRETERIA
class Segreteria(UtenteBase):
    ruolo = models.CharField(max_length=100, default='Segreteria')  # Ruolo fisso per la segreteria

    def __str__(self):
     return self.user.username


    class Meta:
        verbose_name = "segreteria"
        verbose_name_plural = "segreterie"

