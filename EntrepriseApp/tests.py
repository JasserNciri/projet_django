from django.test import TestCase
from django.urls import reverse

from .forms import EntrepriseForm
from .models import Entreprise, Utilisateur


class EntrepriseFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.gerant = Utilisateur.objects.create_user(username="gerant", email="g@gmail.com", password="x")

    def data(self, **overrides):
        d = {
            "raison_sociale": "Chargeur SA",
            "matricule_fiscale": "1234567AAM000",
            "type_entreprise": "chargeur",
            "adresse": "12 rue de la Liberte, Tunis 1000",
            "gerant": self.gerant.pk,
        }
        d.update(overrides)
        return d

    def test_champs_exclus(self):
        form = EntrepriseForm()
        for champ in ("created_at", "updated_at"):
            self.assertNotIn(champ, form.fields)

    def test_form_valide(self):
        form = EntrepriseForm(data=self.data())
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        self.assertEqual(Entreprise.objects.count(), 1)

    def test_champs_obligatoires(self):
        form = EntrepriseForm(data={})
        self.assertFalse(form.is_valid())
        for champ in ("raison_sociale", "matricule_fiscale", "adresse", "gerant"):
            self.assertIn(champ, form.errors)

    def test_matricule_invalide(self):
        form = EntrepriseForm(data=self.data(matricule_fiscale="ABC"))
        self.assertFalse(form.is_valid())
        self.assertIn("matricule_fiscale", form.errors)

    def test_adresse_trop_courte(self):
        form = EntrepriseForm(data=self.data(adresse="Tunis"))
        self.assertFalse(form.is_valid())
        self.assertIn("adresse", form.errors)

    def test_vues_crud(self):
        response = self.client.post(reverse("entreprise:entreprise_create"), self.data())
        self.assertRedirects(response, reverse("entreprise:entreprise_list"))
        entreprise = Entreprise.objects.get()

        self.assertEqual(self.client.get(reverse("entreprise:entreprise_list")).status_code, 200)
        self.assertEqual(self.client.get(reverse("entreprise:entreprise_detail", args=[entreprise.pk])).status_code, 200)

        url = reverse("entreprise:entreprise_update", args=[entreprise.pk])
        self.assertEqual(self.client.get(url).status_code, 200)
        self.client.post(url, self.data(raison_sociale="Nouveau nom"))
        entreprise.refresh_from_db()
        self.assertEqual(entreprise.raison_sociale, "Nouveau nom")

        response = self.client.post(reverse("entreprise:entreprise_delete", args=[entreprise.pk]))
        self.assertRedirects(response, reverse("entreprise:entreprise_list"))
        self.assertFalse(Entreprise.objects.exists())
