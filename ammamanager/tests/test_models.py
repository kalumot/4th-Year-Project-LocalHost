from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from ammamanager.views.ammamanager import SignUpView
from django.contrib.auth.models import User
from ammamanager.models import User

class TestModels(TestCase):

    def setUp(self):
        self.client = Client()

