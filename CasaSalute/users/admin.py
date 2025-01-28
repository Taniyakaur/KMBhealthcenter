from django.contrib import admin
from .models import Paziente, Infermiere, Medico

# Register your models here.
admin.site.register(Paziente)
admin.site.register(Infermiere)
admin.site.register(Medico)
