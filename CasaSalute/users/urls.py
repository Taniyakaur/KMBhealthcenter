from django.urls import path
from .views import (
    login_view, logout_view,
    pagina_medico, modifica_medico, 
    pagina_infermiere, modifica_infermiere, 
    pagina_paziente, prenota_visita,
    pagina_segreteria
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('medico/', pagina_medico, name='medico_dashboard'),
    path('medico/modifica/', modifica_medico, name='modifica_medico'),
    path('infermiere/', pagina_infermiere, name='infermiere_dashboard'),
    path('infermiere/modifica/', modifica_infermiere, name='modifica_infermiere'),
    path('paziente/', pagina_paziente, name='paziente_dashboard'),
    path('paziente/prenota/', prenota_visita, name='prenota_visita'),
    path('segreteria/', pagina_segreteria, name='segreteria_dashboard'),
]
