from django.contrib import admin
from .models import Vehicule


class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('immatriculation', 'type_vehicule', 'capacite_kg', 'disponibilite', 'proprietaire')
    list_filter = ('type_vehicule', 'disponibilite')
    search_fields = ('immatriculation', 'proprietaire__raison_sociale')
    list_editable = ('disponibilite', 'capacite_kg', 'type_vehicule')
    ordering = ('immatriculation',)
    list_per_page = 25
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Identification', {
            'fields': ('immatriculation', 'proprietaire'),
        }),
        ('Caractéristiques', {
            'fields': ('type_vehicule', 'capacite_kg', 'disponibilite'),
        }),
        ('Suivi', {
            'fields': ('created_at', 'updated_at'),
        }),
    )


admin.site.register(Vehicule, VehiculeAdmin)