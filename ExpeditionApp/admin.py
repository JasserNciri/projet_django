from django import forms
from django.contrib import admin, messages
from django.contrib.admin.helpers import ActionForm
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.html import format_html
from .models import Expedition
from OffreApp.models import Offre


class OffreInline(admin.TabularInline):
    model = Offre
    fields = ('transporteur', 'vehicule', 'prix', 'delai_jours', 'statut', 'date_proposition')
    readonly_fields = ('transporteur', 'vehicule', 'prix', 'delai_jours', 'statut', 'date_proposition')
    extra = 0
    show_change_link = True
    can_delete = False


class EnRetardAdmin(admin.SimpleListFilter):
    title = 'Expéditions en retard'
    parameter_name = 'en_retard'

    def lookups(self, request, model_admin):
        return (
            ('oui', 'Oui'),
            ('non', 'Non'),
        )

    def queryset(self, request, queryset):
        aujourd_hui = timezone.now().date()
        if self.value() == 'oui':
            return queryset.filter(statut="publiee", date_souhaitee__lt=aujourd_hui)
        elif self.value() == 'non':
            return queryset.exclude(statut="publiee", date_souhaitee__lt=aujourd_hui)
        return queryset


class StatutActionForm(ActionForm):
    nouveau_statut = forms.ChoiceField(
        choices=[('', '---------')] + list(Expedition._meta.get_field('statut').choices),
        required=False,
        label='Nouveau statut',
    )


class ExpeditionAdmin(admin.ModelAdmin):
    list_display = ('refrence', 'ville_depart', 'ville_arrivee', 'poids_kg',
                    'date_souhaitee', 'statut', 'statut_colore', 'entreprise')
    list_display_links = ('refrence',)
    list_filter = ('statut', 'date_souhaitee', 'ville_depart', 'ville_arrivee', EnRetardAdmin)
    search_fields = ('refrence', 'statut', 'entreprise__raison_sociale')
    list_editable = ('statut', 'ville_depart', 'ville_arrivee', 'poids_kg')
    ordering = ('-created_at',)
    date_hierarchy = 'date_souhaitee'
    list_per_page = 5
    autocomplete_fields = ('entreprise',)
    readonly_fields = ('refrence', 'statut_colore', 'created_at', 'updated_at')
    fieldsets = (
        ('Identification', {
            'fields': ('refrence', 'entreprise', 'description'),
        }),
        ('Trajet', {
            'fields': ('ville_depart', 'ville_arrivee', 'poids_kg', 'date_souhaitee'),
        }),
        ('Suivi', {
            'fields': ('statut', 'statut_colore', 'created_at', 'updated_at'),
        }),
    )
    inlines = [OffreInline]
    action_form = StatutActionForm
    actions = ['cloturer_expeditions', 'changer_statut']

    @admin.display(description='Statut')
    def statut_colore(self, obj):
        couleurs = {
            'publiee': '#5BC0DE',
            'attribuee': '#F0AD4E',
            'en_cours': '#337AB7',
            'livree': '#5CB85C',
            'annulee': '#D9534F',
        }
        return format_html(
            '<span style="color:white;background:{};padding:3px 8px;border-radius:4px;">{}</span>',
            couleurs.get(obj.statut, '#999'), obj.get_statut_display(),
        )

    @admin.action(description="Clôturer les expéditions sélectionnées")
    def cloturer_expeditions(self, request, queryset):
        total = queryset.count()
        traitees = 0
        for expedition in queryset.filter(statut='en_cours'):
            expedition.statut = 'livree'
            try:
                expedition.full_clean()
                expedition.save()
                traitees += 1
            except ValidationError as e:
                self.message_user(request, f"{expedition.refrence} : {e}", messages.ERROR)
        self.message_user(
            request,
            f"{traitees} expédition(s) clôturée(s), {total - traitees} ignorée(s).",
            messages.SUCCESS,
        )

    @admin.action(description="Changer le statut des expéditions sélectionnées")
    def changer_statut(self, request, queryset):
        nouveau_statut = request.POST.get('nouveau_statut')
        if not nouveau_statut:
            self.message_user(request, "Choisis un nouveau statut dans la liste.", messages.WARNING)
            return
        modifiees = 0
        for expedition in queryset.exclude(statut=nouveau_statut):
            ancien_statut = expedition.statut
            expedition.statut = nouveau_statut
            try:
                expedition.full_clean()
                expedition.save()
                modifiees += 1
            except ValidationError as e:
                expedition.statut = ancien_statut
                self.message_user(request, f"{expedition.refrence} : {e}", messages.ERROR)
        libelle = dict(Expedition._meta.get_field('statut').choices)[nouveau_statut]
        self.message_user(
            request,
            f"{modifiees} expédition(s) passée(s) au statut « {libelle} ».",
            messages.SUCCESS,
        )


admin.site.register(Expedition, ExpeditionAdmin)