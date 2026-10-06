from django.db import models
from django.core.validators import MinValueValidator
from EntrepriseApp.models import Entreprise
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
