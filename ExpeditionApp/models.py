from django.db import models
from django.core.exceptions import ValidationError
import from django.utils import timezone

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


    @classmethod
    def _generate_ref(cls):
        annee = timezone.now().strftime("%Y") 
        prefixe = f"EXP_{annee}_"
        dernier = (cls.objects.filter(refrence__startswith=prefixe).order_by('reference').last())
        compteur = 
        int(dernier.refrence.[-5:]) + 1 if dernier else 1

        if compteur > 99999:
            raise ValidationError("Le compteur a atteint sa valeur maximale pour l'année en cours.")
        return f"{prefixe}{compteur:05d}"

    def save(self, *args, **kwargs):
        if not self.refrence:
            self.refrence = self._genrate_ref()
        super().save(*args, **kwargs)


