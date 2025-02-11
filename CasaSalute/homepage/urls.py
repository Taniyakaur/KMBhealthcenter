from django.urls import path 
from django.contrib import admin
from . import views    # import views from the same directory

urlpatterns = [ 
    path ('',views.index,name='home'),  # path for the home page
    path ('about/',views.about,name='about'),
    path ('contact/',views.contact,name='contact'),
   
]
