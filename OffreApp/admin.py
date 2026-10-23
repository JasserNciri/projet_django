import csv
from django.contrib import admin
from django.http import HttpResponse
from .models import Offre


@admin.action(description="Exporter la sélection en CSV")
def exporter_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="offres.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Expedition', 'Transporteur', 'Vehicule', 'Prix', 'Delai (jours)', 'Statut', 'Date de proposition'])
    for offre in queryset.select_related('expedition', 'transporteur', 'vehicule'):
        writer.writerow([offre.id, offre.expedition, offre.transporteur, offre.vehicule,
                         offre.prix, offre.delai_jours, offre.statut, offre.date_proposition])
    return response


class OffreAdmin(admin.ModelAdmin):
    list_display = ('expedition', 'transporteur', 'vehicule', 'prix', 'delai_jours',
                    'statut', 'date_proposition')
    list_display_links = ('expedition',)
    list_filter = ('statut', 'date_proposition')
    search_fields = ('expedition__reference', 'transporteur__raison_sociale')
    list_editable = ('statut',)
    ordering = ('-date_proposition',)
    date_hierarchy = 'date_proposition'
    list_per_page = 25
    autocomplete_fields = ('expedition', 'transporteur', 'vehicule')
    readonly_fields = ('date_proposition', 'created_at', 'updated_at')
    fieldsets = (
        ('Détails de l\'offre', {
            'fields': ('expedition', 'transporteur', 'vehicule'),
        }),
        ('Conditions', {
            'fields': ('prix', 'delai_jours', 'statut'),
        }),
        ('Suivi', {
            'fields': ('date_proposition', 'created_at', 'updated_at'),
        }),
    )
    actions = [exporter_csv]

    def get_readonly_fields(self, request, obj=None):
        base = list(self.readonly_fields)
        if obj and obj.statut == 'acceptee':
            return base + ['prix', 'delai_jours']
        return base


admin.site.register(Offre, OffreAdmin)