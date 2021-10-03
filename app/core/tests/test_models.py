from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email="test@dirox.dev", password="testpass"):
    """Create sample user"""
    return get_user_model().objects.create_user(email, password)


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

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name="Vegan"
        )
        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name="Cucumber"
        )
        self.assertEqual(str(ingredient), ingredient.name)
