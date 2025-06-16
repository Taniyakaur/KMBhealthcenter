from django.contrib import admin
from .models import Visita, PrenotazioneVisita

admin.site.register(Visita)

@admin.register(PrenotazioneVisita)
class PrenotazioneVisitaAdmin(admin.ModelAdmin):
    list_display = ['id', 'paziente', 'medico', 'data', 'ora', 'tipo', 'regime']
    search_fields = ['paziente__nome', 'paziente__cognome', 'medico__nome', 'medico__cognome']
    list_filter = ['tipo', 'regime', 'data']


