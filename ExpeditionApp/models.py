from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Expedition(models.Model):
    refrence = models.CharField(max_length=100, unique=True)
    ville_depart = models.CharField(max_length=100)
    ville_arrivee = models.CharField(max_length=100)
    poids_kg = models.DecimalField(max_digits=10, decimal_places=2)
    date_souhetee = models.DateField()
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('en_attente', 'En attente'),
            ('en_cours', 'En cours'),
            ('terminee', 'Terminée'),
        ],
        default='en_attente'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    entreprise = models.ForeignKey('EntrepriseApp.Entreprise', on_delete=models.CASCADE,
                                   related_name='expeditions')

    def clean (self):
        super().clean()
        if self.entreprise_id and self.entreprise.type_entreprise != 'chargeur':
            raise ValidationError("L'entreprise associée doit être de type 'chargeur'.")