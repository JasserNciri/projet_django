from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Utilisateur (AbstractUser):
    user_id=models.CharField(max_length = 200, primary_key = True)
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=200,
        choices=[
            ('chargeur', 'Chargeur'),
            ('transporteur', 'Transporteur'),
            ('admin', 'Admin'),
        ],
        default='chargeur'
    )
    telephone = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Entreprise(models.Model):
    raison_sociale = models.CharField(max_length=200, null=False,blank=False)
    matricule_fiscale = models.CharField(max_length=17, null=False,blank=False)
    type_entreprise = models.CharField(
        max_length=200,
        choices=[
            ('chargeur', 'Chargeur'),
            ('transporteur', 'Transporteur'),
        ],
        default='chargeur'
    )


    adresse = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True )
    updated_at = models.DateTimeField(auto_now = True)
    gerant =  models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='entreprise')
