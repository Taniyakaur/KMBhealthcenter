from django.urls import path 
from django.contrib import admin
from . import views    # import views from the same directory

urlpatterns = [
    path ('admin/', admin.site.urls),  
    path ('',views.index,name='home'),  # path for the home page
    path ('',views.about,name='about'),
    path ('',views.contact,name='contact'),
   
]