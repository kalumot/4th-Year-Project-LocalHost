from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from ammamanager.views.ammamanager import SignUpView
from django.contrib.auth.models import User
from ammamanager.models import User

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_home_GET(self):
        response = self.client.get(reverse('home'))

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'ammamanager/home.html')

    def test_home_gym_GET(self):
        self.user = User.objects.create_user(
            username='gym1',
            password='pass',
            is_gym=True,
            is_promotion=False
        )
        self.client.login(username='gym1', password='pass')
        response = self.client.get(reverse('home'), follow = True)

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'ammamanager/gyms/gym_home.html', 'base.html')

    def test_home_promotion_GET(self):
        self.user = User.objects.create_user(
            username='prom1',
            password='pass',
            is_gym=False,
            is_promotion=True
        )
        self.client.login(username='prom1', password='pass')
        response = self.client.get(reverse('home'), follow = True)

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'ammamanager/promotions/promotion_home.html', 'promotion_base.html')

    def test_user_gym_security(self):

        response = self.client.get(reverse('gyms:fighter_add'), follow = True)

        self.assertTemplateUsed(response, 'registration/login.html')

    def test_user_promotion_security(self):

        response = self.client.get(reverse('promotions:event_add'), follow = True)

        self.assertTemplateUsed(response, 'registration/login.html')
