from django.test import TestCase
from django.urls import reverse

from .models import CustomUser


class AccountFlowTests(TestCase):
    def test_signup_redirects_with_success_message(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "newmember",
                "email": "newmember@example.com",
                "first_name": "New",
                "last_name": "Member",
                "course": "Information Systems",
                "password1": "A-long-and-unique-pass-8721",
                "password2": "A-long-and-unique-pass-8721",
            },
        )

        self.assertRedirects(
            response, reverse("login"), fetch_redirect_response=False
        )
        login_page = self.client.get(reverse("login"))
        self.assertContains(login_page, "Your account is ready.")
        self.assertTrue(CustomUser.objects.filter(username="newmember").exists())

    def test_profile_requires_login(self):
        response = self.client.get(reverse("profile"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('profile')}",
        )

    def test_profile_updates_only_signed_in_user(self):
        user = CustomUser.objects.create_user(
            username="member", password="A-long-and-unique-pass-8721"
        )
        other_user = CustomUser.objects.create_user(
            username="other", password="A-long-and-unique-pass-8721"
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse("profile"),
            {
                "first_name": "Campus",
                "last_name": "Member",
                "email": "campus@example.com",
                "course": "Design",
            },
        )

        self.assertRedirects(response, reverse("profile"))
        user.refresh_from_db()
        other_user.refresh_from_db()
        self.assertEqual(user.first_name, "Campus")
        self.assertEqual(user.email, "campus@example.com")
        self.assertEqual(user.course, "Design")
        self.assertEqual(other_user.first_name, "")
