from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, Medico, Infermiere, Paziente, Segreteria

@receiver(post_save, sender=UserProfile)
def crea_utente_specifico(sender, instance, created, **kwargs):
    if created:
        if instance.tipo_utente == 'medico' and not Medico.objects.filter(user=instance.user).exists():
            Medico.objects.create(user=instance.user)
        elif instance.tipo_utente == 'infermiere' and not Infermiere.objects.filter(user=instance.user).exists():
            Infermiere.objects.create(user=instance.user)
        elif instance.tipo_utente == 'paziente' and not Paziente.objects.filter(user=instance.user).exists():
            Paziente.objects.create(
                user=instance.user,
                nome=instance.user.first_name,
                cognome=instance.user.last_name,
                codice_fiscale='DADEFINIRE',
                data_nascita='1000-01-01',
                luogo_nascita='Da definire',
                email=instance.user.email
            )
        elif instance.tipo_utente == 'segreteria' and not Segreteria.objects.filter(user=instance.user).exists():
            Segreteria.objects.create(user=instance.user)