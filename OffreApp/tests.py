from datetime import date

from django.test import TestCase
from django.urls import reverse

from EntrepriseApp.models import Entreprise, Utilisateur
from ExpeditionApp.models import Expedition
from VehiculeApp.models import Vehicule
from .forms import OffreForm
from .models import Offre


class OffreFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = Utilisateur.objects.create_user(username="chargeur", email="c@gmail.com", password="x")
        user2 = Utilisateur.objects.create_user(username="transp", email="t@gmail.com", password="x")
        cls.chargeur = Entreprise.objects.create(
            raison_sociale="Chargeur SA", matricule_fiscale="1234567AAM000",
            type_entreprise="chargeur", adresse="12 rue de la Liberte, Tunis 1000", gerant=user1,
        )
        cls.transporteur = Entreprise.objects.create(
            raison_sociale="Transport SA", matricule_fiscale="7654321BAM000",
            type_entreprise="transporteur", adresse="45 avenue Habib Bourguiba, Sfax", gerant=user2,
        )
        cls.expedition = Expedition.objects.create(
            ville_depart="Tunis", ville_arrivee="Sfax", poids_kg="150.50",
            date_souhaitee=date(2026, 12, 1), description="Palettes", entreprise=cls.chargeur,
        )
        cls.vehicule = Vehicule.objects.create(
            immatriculation="123 TU 4567", type_vehicule="camionette", capacite_kg=1200,
            proprietaire=cls.transporteur,
        )

    def data(self, **overrides):
        d = {
            "prix": "500.00",
            "delai_jours": 3,
            "statut": "proposee",
            "expedition": self.expedition.pk,
            "transporteur": self.transporteur.pk,
            "vehicule": self.vehicule.pk,
        }
        d.update(overrides)
        return d

    def test_champs_exclus(self):
        form = OffreForm()
        for champ in ("created_at", "updated_at", "date_proposition"):
            self.assertNotIn(champ, form.fields)

    def test_form_valide(self):
        form = OffreForm(data=self.data())
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        self.assertEqual(Offre.objects.count(), 1)

    def test_champs_obligatoires(self):
        form = OffreForm(data={})
        self.assertFalse(form.is_valid())
        for champ in ("prix", "delai_jours", "expedition", "transporteur", "vehicule"):
            self.assertIn(champ, form.errors)

    def test_prix_nul_refuse(self):
        form = OffreForm(data=self.data(prix="0"))
        self.assertFalse(form.is_valid())
        self.assertIn("prix", form.errors)

    def test_delai_nul_refuse(self):
        form = OffreForm(data=self.data(delai_jours=0))
        self.assertFalse(form.is_valid())
        self.assertIn("delai_jours", form.errors)

    def test_transporteur_chargeur_refuse(self):
        form = OffreForm(data=self.data(transporteur=self.chargeur.pk))
        self.assertFalse(form.is_valid())

    def test_vues_crud(self):
        response = self.client.post(reverse("offre:offre_create"), self.data())
        self.assertRedirects(response, reverse("offre:offre_list"))
        offre = Offre.objects.get()

        self.assertEqual(self.client.get(reverse("offre:offre_list")).status_code, 200)
        self.assertEqual(self.client.get(reverse("offre:offre_detail", args=[offre.pk])).status_code, 200)

        url = reverse("offre:offre_update", args=[offre.pk])
        self.assertEqual(self.client.get(url).status_code, 200)
        self.client.post(url, self.data(prix="450.00"))
        offre.refresh_from_db()
        self.assertEqual(str(offre.prix), "450.00")

        response = self.client.post(reverse("offre:offre_delete", args=[offre.pk]))
        self.assertRedirects(response, reverse("offre:offre_list"))
        self.assertFalse(Offre.objects.exists())

    def test_suppression_vehicule_protege(self):
        OffreForm(data=self.data()).save()
        response = self.client.post(reverse("vehicule:vehicule_delete", args=[self.vehicule.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Suppression impossible")
        self.assertTrue(Vehicule.objects.filter(pk=self.vehicule.pk).exists())
