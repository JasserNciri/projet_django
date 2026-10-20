from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import transaction
from django.utils import timezone


POIDS_PAR_TYPE = {
    'camionette': (0, 1500),
    'fourgon': (0, 3500),
    'camionporteur': (3500, 19000),
    'semi-remorque': (19000, 26000),
}


class Offre(models.Model):
    prix = models.DecimalField(max_digits=10, decimal_places=2,
                               validators=[MinValueValidator(Decimal('0.01'), "Le prix doit être strictement positif.")])
    delai_jours = models.PositiveIntegerField(
        validators=[MinValueValidator(1, "Le délai doit être d'au moins 1 jour.")])
    statut = models.CharField(
        max_length=20,
        choices=[
            ('proposee', 'Proposée'),
            ('acceptee', 'Acceptée'),
            ('refusee', 'Refusée'),
            ('retiree', 'Retirée'),
        ],
        default='proposee'
    )
    date_proposition = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expedition = models.ForeignKey('ExpeditionApp.Expedition', on_delete=models.CASCADE,
                                   related_name='offres')
    transporteur = models.ForeignKey('EntrepriseApp.Entreprise', on_delete=models.CASCADE,
                                     related_name='offres')
    vehicule = models.ForeignKey('VehiculeApp.Vehicule', on_delete=models.PROTECT,
                                 related_name='offres')

    def clean(self):
        # règle 1
        super().clean()
        if self.transporteur_id and self.transporteur.type_entreprise != 'transporteur':
            raise ValidationError("L'entreprise associée doit être de type 'transporteur'.")

        # règle 2
        if self.vehicule_id and self.transporteur_id and self.vehicule.proprietaire_id != self.transporteur_id:
            raise ValidationError("Le véhicule doit appartenir à l'entreprise transporteur.")

        if not (self.expedition_id and self.transporteur_id and self.vehicule_id):
            return

        if self._state.adding and self.expedition.statut != 'publiee':
            raise ValidationError("Cette expédition n'accepte plus de nouvelles offres (statut différent de 'publiee').")

        if (self.statut == 'proposee'
                and Offre.objects.filter(expedition=self.expedition, transporteur=self.transporteur,
                                         statut='proposee').exclude(pk=self.pk).exists()):
            raise ValidationError("Ce transporteur a déjà une offre 'proposee' active sur cette expédition.")

        if self._state.adding and not self.vehicule.disponibilite:
            raise ValidationError("Ce véhicule n'est pas disponible.")

        if self.vehicule.type_vehicule in POIDS_PAR_TYPE:
            poids_min, poids_max = POIDS_PAR_TYPE[self.vehicule.type_vehicule]
            if not (poids_min <= self.expedition.poids_kg <= poids_max):
                raise ValidationError("Ce type de véhicule n'est pas compatible avec le poids de l'expédition.")

    def save(self, *args, **kwargs):
        with transaction.atomic():
            self.full_clean()
            super().save(*args, **kwargs)
            if self.statut == 'acceptee':
                self.expedition.statut = 'attribuee'
                self.expedition.save()
                Offre.objects.filter(expedition=self.expedition, statut='proposee').exclude(pk=self.pk).update(
                    statut='refusee', updated_at=timezone.now())

    def __str__(self):
        return f"Offre {self.pk} - {self.expedition}"