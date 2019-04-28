from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ammamanager.views.ammamanager import SignUpView

class TestUrls(SimpleTestCase):

    def test_signup_url_is_resolved(self):
        url = reverse('signup')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, SignUpView)
