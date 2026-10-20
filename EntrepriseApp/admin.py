from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Entreprise, Utilisateur
from VehiculeApp.models import Vehicule

admin.site.site_header = "Transconnect - Administration"
admin.site.site_title = "Transconnect"
admin.site.index_title = "Tableau de bord"


class vehiculeInline(admin.TabularInline):
    model = Vehicule
    fields = ('immatriculation', 'type_vehicule', 'capacite_kg', 'disponibilite')
    extra = 1
    show_change_link = True


class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ('raison_sociale', 'adresse', 'matricule_fiscale', 'type_entreprise', 'gerant')
    list_filter = ('type_entreprise',)
    search_fields = ('raison_sociale', 'matricule_fiscale', 'adresse')
    list_editable = ('type_entreprise',)
    ordering = ('raison_sociale',)
    list_per_page = 25
    fieldsets = (
        ('Informations générales', {
            'fields': ('raison_sociale', 'type_entreprise', 'matricule_fiscale', 'gerant'),
        }),
        ('Coordonnées', {
            'fields': ('adresse',),
        }),
    )
    inlines = [vehiculeInline]


class UtilisateurAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'first_name', 'last_name', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    fieldsets = UserAdmin.fieldsets + (
        ('Informations TransConnect', {
            'fields': ('role', 'telephone'),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'telephone',
                       'usable_password', 'password1', 'password2'),
        }),
    )


admin.site.register(Entreprise, EntrepriseAdmin)
admin.site.register(Utilisateur, UtilisateurAdmin)