from django import forms
from .models import Vehicule

class VehiculeForm(forms.ModelForm):
    class Meta:
        model = Vehicule
        fields = "__all__"
        exclude = ['created_at', 'updated_at']
