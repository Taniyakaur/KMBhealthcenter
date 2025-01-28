from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="prestazione_index"),
    path("create/", views.create, name="prestazione_create"),
    path("update/<int:id>/", views.update, name="prestazione_update"),
    path("delete/<int:id>/", views.delete, name="prestazione_delete"),
    path("<int:id>/", views.detail, name="prestazione_detail"),
]