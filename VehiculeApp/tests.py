from django.test import TestCase
from django.urls import reverse

from EntrepriseApp.models import Entreprise, Utilisateur
from .forms import VehiculeForm
from .models import Vehicule


class VehiculeFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = Utilisateur.objects.create_user(username="transp", email="t@gmail.com", password="x")
        user2 = Utilisateur.objects.create_user(username="chargeur", email="c@gmail.com", password="x")
        cls.transporteur = Entreprise.objects.create(
            raison_sociale="Transport SA", matricule_fiscale="7654321BAM000",
            type_entreprise="transporteur", adresse="45 avenue Habib Bourguiba, Sfax", gerant=user1,
        )
        cls.chargeur = Entreprise.objects.create(
            raison_sociale="Chargeur SA", matricule_fiscale="1234567AAM000",
            type_entreprise="chargeur", adresse="12 rue de la Liberte, Tunis 1000", gerant=user2,
        )

    def data(self, **overrides):
        d = {
            "immatriculation": "123 TU 4567",
            "type_vehicule": "camionette",
            "capacite_kg": 1200,
            "disponibilite": True,
            "proprietaire": self.transporteur.pk,
        }
        d.update(overrides)
        return d

    def test_champs_exclus(self):
        form = VehiculeForm()
        for champ in ("created_at", "updated_at"):
            self.assertNotIn(champ, form.fields)

    def test_form_valide(self):
        form = VehiculeForm(data=self.data())
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        self.assertEqual(Vehicule.objects.count(), 1)

    def test_champs_obligatoires(self):
        form = VehiculeForm(data={})
        self.assertFalse(form.is_valid())
        for champ in ("immatriculation", "capacite_kg", "proprietaire"):
            self.assertIn(champ, form.errors)

    def test_capacite_trop_faible(self):
        form = VehiculeForm(data=self.data(capacite_kg=50))
        self.assertFalse(form.is_valid())
        self.assertIn("capacite_kg", form.errors)

    def test_proprietaire_chargeur_refuse(self):
        form = VehiculeForm(data=self.data(proprietaire=self.chargeur.pk))
        self.assertFalse(form.is_valid())

    def test_vues_crud(self):
        response = self.client.post(reverse("vehicule:vehicule_create"), self.data())
        self.assertRedirects(response, reverse("vehicule:vehicule_list"))
        vehicule = Vehicule.objects.get()

        self.assertEqual(self.client.get(reverse("vehicule:vehicule_list")).status_code, 200)
        self.assertEqual(self.client.get(reverse("vehicule:vehicule_detail", args=[vehicule.pk])).status_code, 200)

        url = reverse("vehicule:vehicule_update", args=[vehicule.pk])
        self.assertEqual(self.client.get(url).status_code, 200)
        self.client.post(url, self.data(capacite_kg=1400))
        vehicule.refresh_from_db()
        self.assertEqual(vehicule.capacite_kg, 1400)

        response = self.client.post(reverse("vehicule:vehicule_delete", args=[vehicule.pk]))
        self.assertRedirects(response, reverse("vehicule:vehicule_list"))
        self.assertFalse(Vehicule.objects.exists())
