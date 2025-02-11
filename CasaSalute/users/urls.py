from django.urls import path
from .views import (
    pagina_medico, modifica_medico, 
    pagina_infermiere, modifica_infermiere, 
    pagina_paziente, prenota_visita
)

urlpatterns = [
    path('medico/', pagina_medico, name='pagina_medico'),
    path('medico/modifica/', modifica_medico, name='modifica_medico'),
    path('infermiere/', pagina_infermiere, name='pagina_infermiere'),
    path('infermiere/modifica/', modifica_infermiere, name='modifica_infermiere'),
    path('paziente/', pagina_paziente, name='pagina_paziente'),
    path('paziente/prenota/', prenota_visita, name='prenota_visita'),
]


