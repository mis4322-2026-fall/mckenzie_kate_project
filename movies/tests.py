import secrets
from django.contrib.auth import SESSION_KEY, get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class AuthenticationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = secrets.token_urlsafe(24)
        cls.user = get_user_model().objects.create_user("demo_viewer", password=cls.password)

    def sign_in(self, client=None):
        return (client or self.client).post(reverse("login"), {"username": self.user.username, "password": self.password})

    def test_public_welcome_and_login(self):
        self.assertContains(self.client.get(reverse("welcome")), "Welcome to Movie Finder")
        self.assertContains(self.client.get(reverse("login")), "csrfmiddlewaretoken")

    def test_anonymous_dashboard_redirects(self):
        self.assertRedirects(self.client.get(reverse("dashboard")), "/accounts/login/?next=/dashboard/")

    def test_valid_login_opens_dashboard(self):
        self.assertRedirects(self.sign_in(), reverse("dashboard"))
        self.assertIn(SESSION_KEY, self.client.session)
        self.assertContains(self.client.get(reverse("dashboard")), self.user.username)

    def test_invalid_credentials_do_not_grant_access(self):
        response = self.client.post(reverse("login"), {"username": self.user.username, "password": "incorrect"})
        self.assertContains(response, "Please enter a correct username and password")
        self.assertNotIn(SESSION_KEY, self.client.session)
        self.assertRedirects(self.client.get(reverse("dashboard")), "/accounts/login/?next=/dashboard/")

    def test_post_logout_ends_access(self):
        self.sign_in()
        self.assertRedirects(self.client.post(reverse("logout")), reverse("welcome"))
        self.assertNotIn(SESSION_KEY, self.client.session)
        self.assertRedirects(self.client.get(reverse("dashboard")), "/accounts/login/?next=/dashboard/")

    def test_get_logout_is_rejected(self):
        self.sign_in()
        self.assertEqual(self.client.get(reverse("logout")).status_code, 405)
        self.assertIn(SESSION_KEY, self.client.session)

    def test_csrf_is_required_for_login_and_logout(self):
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(self.sign_in(client).status_code, 403)
        client.get(reverse("login"))
        token = client.cookies["csrftoken"].value
        response = client.post(reverse("login"), {"username": self.user.username, "password": self.password, "csrfmiddlewaretoken": token})
        self.assertRedirects(response, reverse("dashboard"))
        self.assertEqual(client.post(reverse("logout")).status_code, 403)
        client.get(reverse("dashboard"))
        token = client.cookies["csrftoken"].value
        self.assertRedirects(client.post(reverse("logout"), {"csrfmiddlewaretoken": token}), reverse("welcome"))
        self.assertNotIn(SESSION_KEY, client.session)

    def test_login_does_not_redirect_to_external_site(self):
        response = self.client.post(reverse("login"), {"username": self.user.username, "password": self.password, "next": "https://example.com/"})
        self.assertRedirects(response, reverse("dashboard"))
