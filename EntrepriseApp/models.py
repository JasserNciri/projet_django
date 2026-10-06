from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator,MaxLengthValidator
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# Create your models here.

matricule_fiscale_validator = RegexValidator(
    regex=r'^\d{7}[/ -]?[A-Za-z][/ -]?[ABDNPEabdnpe][/ -]?[MPCNEmpcne][/ -]?\d{3}$'
    message="Format incorrect -(ex,1234567AAM000 OU 1234567-A-A-M-000)."
)

def validate_email(value):
    if not value :
        raise ValidationError("L'adresse e-mail est obligatoire.")
    if not value .endswith('@gmail.com'):
        raise ValidationError("L'adresse e-mail doit se terminer par '@gmail.com'.")

class Utilisateur (AbstractUser):
    user_id=models.CharField(max_length = 200, primary_key = True)
    email = models.EmailField(unique=True, validators=[validate_email])
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
    matricule_fiscale = models.CharField(max_length=17, unique=True, 
                                         validators=[matricule_fiscale_validator])
    type_entreprise = models.CharField(
        max_length=200,
        choices=[
            ('chargeur', 'Chargeur'),
            ('transporteur', 'Transporteur'),
        ],
        default='chargeur'
    )


    adresse = models.TextField(validators=MinLengthValidator(20,"l adresse doit avoir au moins 20 char"),
                               MaxLengthValidator(300, "l adresse ne peut pas passer les 300 char "))
    created_at = models.DateTimeField(auto_now_add = True )
    updated_at = models.DateTimeField(auto_now = True)
    gerant =  models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='entreprise')
