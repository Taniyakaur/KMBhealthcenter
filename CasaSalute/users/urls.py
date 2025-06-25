from django.urls import path
from .views import (
    login_view, logout_view,
    pagina_medico, modifica_medico, 
    pagina_infermiere, modifica_infermiere, 
    pagina_paziente, prenota_visita,
    pagina_segreteria, inserisci_esito_visita, resoconto_paziente,
    prestazioni_infermiere  
)


urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Medico
    path('medico/', pagina_medico, name='pagina_medico'),
    path('medico/modifica/', modifica_medico, name='modifica_medico'),

    # Infermiere
    path('infermiere/', pagina_infermiere, name='pagina_infermiere'),
    path('infermiere/modifica/', modifica_infermiere, name='modifica_infermiere'),
    path('infermiere/prestazioni/', prestazioni_infermiere, name='prestazioni_infermiere'),

    # Paziente
    path('paziente/', pagina_paziente, name='pagina_paziente'),
    path('paziente/prenota/', prenota_visita, name='prenota_visita'),

    # Segreteria
    path('segreteria/', pagina_segreteria, name='segreteria_dashboard'),
    path('segreteria/inserisci-esito-visita/', inserisci_esito_visita, name='inserisci_esito_visita'),
    path('segreteria/resoconto-paziente/', resoconto_paziente, name='resoconto_paziente'),
]
