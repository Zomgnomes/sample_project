from apps.users.models import User
from django.test import TestCase
from rest_framework.test import APIClient


class UserTestCase(TestCase):
    """Tests related to the User model."""

    def setUp(self):
        """Set up required items for the tests."""
        super().setUp()

        self.user = User.objects.create(
            email="test@test.com",
            password="password",
        )

    def tearDown(self):
        """Clean up items from the setup method."""
        self.user.delete()

    def test_authenticated_user_can_get_users(self):
        """Authenticated users can query the users endpoint."""
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get("/api/users/")
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_user_cannot_get_users(self):
        """Unauthenticated users cannot query the users endpoint."""
        client = APIClient()
        response = client.get("/api/users/")
        self.assertEqual(response.status_code, 403)
