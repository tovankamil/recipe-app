"""
Test for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test Models"""

    def test_create_user_with_email_successfull(self):
        """Test creating a user"""
        email = "test@example.com"
        password = "test123"

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            name="Test User"
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """
        Test email is normalized (lowercased) for new user
        """
        sample_emails = [
            ['TeSt@EXAMPLE.com', 'test@example.com'],
            ['OTHER@DOMAIN.COM', 'other@domain.com'],
        ]

        password = "test123"
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                email=email,
                password=password,
                name="Temp User"
            )
            self.assertEqual(user.email, expected)

    def test_create_superuser_success(self):
        """Test creating a superuser is successful."""
        email = 'admin@example.com'
        password = 'supersecurepassword'

        user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
            name='Admin User'  # Tambahkan field wajib
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.email, email)

    def test_new_user_without_email(self):
        """Test that creating a user without email user"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email="",  # Test case for missing email
                password="12312",
                name="Validation Test"
            )

    def test_create_superuser(self):
        """Test Creating a superuser"""
        user = get_user_model().objects.create_superuser(
            email='test@example.com',
            password='test123',
            name='Test Admin'  # Menambahkan field wajib yang hilang
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
