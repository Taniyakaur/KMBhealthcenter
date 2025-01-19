from django.urls import path 
from . import views    # import views from the same directory

urlpatterns = [
    path('', views.index, name='index'),    # path for the home page
    path('<str:name>', views.greet, name='greet'),    # path for the greet
    path('taniya', views.taniya, name='taniya')    # path for the taniya page
]