from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="visita_index"),
    path("create/", views.create_visita, name="create_visita"),
    path("update/<int:id>/", views.update, name="visita_update"),
    path("delete/<int:id>/", views.delete, name="visita_delete"),
    path("<int:id>/", views.detail, name="visita_detail"),
]