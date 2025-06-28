from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date
from users.models import Paziente

class PazienteViewTest(TestCase):
    def setUp(self):
        # Crea utente
        self.user = User.objects.create_user(username='andrearusso10', password='password123')

        # Crea paziente associato
        self.paziente = Paziente.objects.create(
            user=self.user,
            nome='Andrea',
            cognome='Russo',
            codice_fiscale='BRCRCC',
            data_nascita=date(2002, 1, 1),
            luogo_nascita='Verona',
            email='andrearusso10@example.com'
        )

        self.client = Client()

    def test_pagina_paziente_contenuto(self):
        # Effettua login
        self.client.login(username='andrearusso10', password='password123')

        # Visita la pagina del paziente
        response = self.client.get(reverse('pagina_paziente'))

        # Controlli base
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Andrea')
        self.assertContains(response, 'Russo')
