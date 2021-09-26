from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successfull(self):
        """Test creating a new user with an email is successfull"""
        email = "superuser@dirox.dev"
        password = "Testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normailized"""
        email = "test@DIROX.NET"
        user = get_user_model().objects.create_user(email, password="test123")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, password="test123")

    def test_create_superuser(self):
        """Test creating new super user"""
        super_user = get_user_model().objects.create_superuser(
            "superuser@dirox.net",
            "test123"
        )
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_superuser)