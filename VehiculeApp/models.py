from django.db import models
from django.core.validators import MinValueValidator
from EntrepriseApp.models import Entreprise
from django.core.exceptions import ValidationError 


# Create your models here.


class Vehicule(models.Model):
    immatriculation = models.CharField(max_length=20, unique=True)
    type_vehicule = models.CharField(max_length=50,
                                     choices=[
                                         ('camionette', 'Camionnette'),
                                         ('camionporteur', 'Camion Porteur'),
                                         ('semi-remorque', 'Semi-Remorque'),
                                         ('fourgon', 'Fourgon'),
                                     ],default='camionette')
    capacite_kg = models.IntegerField(validators=[MinValueValidator(100,"capacite doit etre sup a 100 kg ")])
    disponibilite = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    proprietaire = models.ForeignKey('EntrepriseApp.Entreprise', on_delete=models.CASCADE, 
                                     related_name='vehicules')

    def clean(self):
        super().clean()
        if self.proprietaire_id and self.proprietaire.type_entreprise != 'transporteur':
            raise ValidationError("L'entreprise associée doit être de type 'transporteur'.")


    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)

    def __str__(self):
        return self.immatriculation