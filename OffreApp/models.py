from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Offre(models.Model):
   prix = models.DecimalField(max_digits=10, decimal_places=2)
   deliai_jours = models.IntegerField()
   status = models.CharField(
       max_length=20,   
       choices=[
           ('en_attente', 'En attente'),
           ('acceptee', 'Acceptée'),
           ('refusee', 'Refusée'),
       ],
       default='en_attente'
   )    
   date_propsition = models.DateTimeField(auto_now_add=True)
   creted_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)
   expedition = models.ForeignKey('ExpeditionApp.Expedition', on_delete=models.CASCADE, 
                                  related_name='offres')
   transporteur = models.ForeignKey('EntrepriseApp.Entreprise', on_delete=models.CASCADE,
                                   related_name='offres')
   expedition = models.ForeignKey('ExpeditionApp.Expedition', on_delete=models.CASCADE, 
                                  related_name='offres')
   vehicule = models.ForeignKey('VehiculeApp.Vehicule', on_delete=models.CASCADE,
                               related_name='offres')
   def clean(self):
       #regles 1
       super().clean()
       if self.transporteur_id and self.transporteur.type_entreprise != 'transporteur':
           raise ValidationError("L'entreprise associée doit être de type 'transporteur'.")
         
       #regles 2

       if self.vehicule_id and self.transporteur_id and self.vehicule.proprietaire_id != self.transporteur_id:
           raise ValidationError("Le véhicule doit appartenir à l'entreprise transporteur transproteur.")
