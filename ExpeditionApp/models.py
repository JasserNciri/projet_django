from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal


class Expedition(models.Model):
    reference = models.CharField(max_length=100, unique=True, blank=True)
    ville_depart = models.CharField(max_length=100)
    ville_arrivee = models.CharField(max_length=100)
    poids_kg = models.DecimalField(max_digits=10, decimal_places=2,
                                   validators=[MinValueValidator(Decimal('0.01'), "Le poids ne peut pas être nul.")])
    date_souhaitee = models.DateField()
    description = models.TextField()
    statut = models.CharField(
        max_length=20,
        choices=[
            ('publiee', 'Publiée'),
            ('attribuee', 'Attribuée'),
            ('en_cours', 'En cours'),
            ('livree', 'Livrée'),
            ('annulee', 'Annulée'),
        ],
        default='publiee'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    entreprise = models.ForeignKey('EntrepriseApp.Entreprise', on_delete=models.CASCADE,
                                   related_name='expeditions')

    def clean(self):
        super().clean()
        if self.entreprise_id and self.entreprise.type_entreprise != 'chargeur':
            raise ValidationError("L'entreprise associée doit être de type 'chargeur'.")

    @classmethod
    def _generate_ref(cls):
        annee = timezone.now().strftime("%y")
        prefixe = f"EXP-{annee}-"
        dernier = cls.objects.filter(reference__startswith=prefixe).order_by('reference').last()
        compteur = int(dernier.reference[-5:]) + 1 if dernier else 1
        if compteur > 99999:
            raise ValidationError("Le compteur a atteint sa valeur maximale pour l'année en cours.")
        return f"{prefixe}{compteur:05d}"

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self._generate_ref()
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.reference