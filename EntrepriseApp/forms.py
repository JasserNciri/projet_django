from django import forms
from .models import Entreprise

class EntrepriseForm(forms.ModelForm):
    class Meta:
        model = Entreprise
        fields = "__all__"
        exclude = ['created_at', 'updated_at']
