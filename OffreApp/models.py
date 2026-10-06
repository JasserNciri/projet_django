from django.db import models

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