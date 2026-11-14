from django import forms
from .models import Offre

class OffreForm(forms.ModelForm):
    class Meta:
        model = Offre
        fields = "__all__"
        exclude = ['created_at', 'updated_at', 'date_proposition']
