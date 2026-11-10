from datetime import date

from django.test import TestCase
from django.urls import reverse

from EntrepriseApp.models import Entreprise, Utilisateur
from .forms import ExpeditionForm
from .models import Expedition


class ExpeditionFormTests(TestCase):
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

    def data(self, **overrides):
        d = {
            "ville_depart": "Tunis",
            "ville_arrivee": "Sfax",
            "poids_kg": "150.50",
            "date_souhaitee": date(2026, 12, 1),
            "description": "Palettes de marchandises",
            "entreprise": self.chargeur.pk,
        }
        d.update(overrides)
        return d

    def test_champs_exclus(self):
        form = ExpeditionForm()
        for champ in ("reference", "created_at", "updated_at", "statut"):
            self.assertNotIn(champ, form.fields)

    def test_form_valide(self):
        form = ExpeditionForm(data=self.data())
        self.assertTrue(form.is_valid(), form.errors)
        expedition = form.save()
        self.assertTrue(expedition.reference.startswith("EXP-"))
        self.assertEqual(expedition.statut, "publiee")

    def test_champs_obligatoires(self):
        form = ExpeditionForm(data={})
        self.assertFalse(form.is_valid())
        for champ in ("ville_depart", "ville_arrivee", "poids_kg", "date_souhaitee", "description", "entreprise"):
            self.assertIn(champ, form.errors)

    def test_poids_nul_refuse(self):
        form = ExpeditionForm(data=self.data(poids_kg="0"))
        self.assertFalse(form.is_valid())
        self.assertIn("poids_kg", form.errors)

    def test_poids_negatif_refuse(self):
        form = ExpeditionForm(data=self.data(poids_kg="-5"))
        self.assertFalse(form.is_valid())
        self.assertIn("poids_kg", form.errors)

    def test_date_invalide(self):
        form = ExpeditionForm(data=self.data(date_souhaitee="pas-une-date"))
        self.assertFalse(form.is_valid())
        self.assertIn("date_souhaitee", form.errors)

    def test_entreprise_transporteur_refusee(self):
        form = ExpeditionForm(data=self.data(entreprise=self.transporteur.pk))
        self.assertFalse(form.is_valid())

    def test_vue_creation_get(self):
        response = self.client.get(reverse("expedition:expedition_create"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], ExpeditionForm)

    def test_vue_creation_post(self):
        response = self.client.post(reverse("expedition:expedition_create"), self.data())
        self.assertRedirects(response, reverse("expedition:list"))
        self.assertEqual(Expedition.objects.count(), 1)

    def test_vue_modification(self):
        expedition = ExpeditionForm(data=self.data()).save()
        url = reverse("expedition:expedition_update", args=[expedition.pk])
        self.assertEqual(self.client.get(url).status_code, 200)
        response = self.client.post(url, self.data(ville_arrivee="Sousse", poids_kg="300"))
        self.assertRedirects(response, reverse("expedition:list"))
        expedition.refresh_from_db()
        self.assertEqual(expedition.ville_arrivee, "Sousse")
        self.assertEqual(Expedition.objects.count(), 1)
