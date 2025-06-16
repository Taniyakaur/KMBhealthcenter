from django.contrib import admin
from .models import Prestazione, PrenotazionePrestazione

@admin.register(Prestazione)
class PrestazioneAdmin(admin.ModelAdmin):
    list_display = ['id', 'tipo', 'paziente', 'ambulatorio', 'infermiere', 'data']
    search_fields = ['paziente__nome', 'paziente__cognome', 'tipo']
    list_filter = ['tipo', 'data']

@admin.register(PrenotazionePrestazione)
class PrenotazionePrestazioneAdmin(admin.ModelAdmin):
    list_display = ['id', 'tipo', 'paziente', 'data', 'orario']
    search_fields = ['paziente__nome', 'paziente__cognome', 'tipo']
    list_filter = ['tipo', 'data']

    
