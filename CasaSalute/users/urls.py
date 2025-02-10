from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("medico", views.medico_view, name="medico"),
    path("infermiere", views.infermiere_view, name="infermiere"),
    path("paziente", views.paziente_view, name="paziente"),
]