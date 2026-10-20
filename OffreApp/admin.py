import csv
from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
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
                    'statut', 'statut_colore', 'date_proposition')
    list_display_links = ('expedition',)
    list_filter = ('statut', 'date_proposition')
    search_fields = ('expedition__refrence', 'transporteur__raison_sociale')
    list_editable = ('statut',)
    ordering = ('-date_proposition',)
    date_hierarchy = 'date_proposition'
    list_per_page = 25
    autocomplete_fields = ('expedition', 'transporteur', 'vehicule')
    readonly_fields = ('statut_colore', 'date_proposition', 'created_at', 'updated_at')
    fieldsets = (
        ('Détails de l\'offre', {
            'fields': ('expedition', 'transporteur', 'vehicule'),
        }),
        ('Conditions', {
            'fields': ('prix', 'delai_jours', 'statut'),
        }),
        ('Suivi', {
            'fields': ('statut_colore', 'date_proposition', 'created_at', 'updated_at'),
        }),
    )
    actions = [exporter_csv]

    @admin.display(description='Statut')
    def statut_colore(self, obj):
        couleurs = {
            'proposee': '#F0AD4E',
            'acceptee': '#5CB85C',
            'refusee': '#D9534F',
            'retiree': '#777777',
        }
        return format_html(
            '<span style="color:white;background:{};padding:3px 8px;border-radius:4px;">{}</span>',
            couleurs.get(obj.statut, '#999'), obj.get_statut_display(),
        )

    def get_readonly_fields(self, request, obj=None):
        base = list(self.readonly_fields)
        if obj and obj.statut == 'acceptee':
            return base + ['prix', 'delai_jours']
        return base


admin.site.register(Offre, OffreAdmin)