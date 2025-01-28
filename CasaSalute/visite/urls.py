# filepath: /Users/taniyakaur/Documents/GitHub/Project/CasaSalute/visite/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="visite_index"),
    path("create/", views.create, name="visite_create"),
    path("update/<int:id>/", views.update, name="visite_update"),
    path("delete/<int:id>/", views.delete, name="visite_delete"),
    path("<int:id>/", views.detail, name="visite_detail"),
]