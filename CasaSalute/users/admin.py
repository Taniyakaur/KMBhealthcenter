from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Paziente, Infermiere, Medico, Segreteria, AssenzaPianificata, UserProfile

@admin.register(Paziente)
class PazienteAdmin(admin.ModelAdmin):
    list_display = ('user', 'nome', 'cognome')

@admin.register(Infermiere)
class InfermiereAdmin(admin.ModelAdmin):
    list_display = ('user','nome', 'cognome')


@admin.register(Segreteria)
class SegreteriaAdmin(admin.ModelAdmin):
    list_display = ('user','nome', 'cognome')

class AssenzaPianificataInline(admin.TabularInline):
    model = AssenzaPianificata
    extra = 1

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    inlines = [AssenzaPianificataInline]
    search_fields = ('user__username', 'specializzazione')
    list_filter = ('specializzazione',)
    ordering = ('user__username',)
    list_display = ('user', 'nome', 'cognome','specializzazione')


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

