"""
Test for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    """Test Models"""
    
    def test_create_user_with_email_successfull(self):
        """Test creating a user with email is successful and checks password."""
        email = "test@example.com"
        password = "test123"
        # Karena Anda menggunakan AbstractBaseUser, HAPUS argumen 'username'.
        # Saya menambahkan field 'name' karena biasanya ada di REQUIRED_FIELDS.
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            name="Test User" # Tambahkan field wajib jika ada di REQUIRED_FIELDS
        )
        
        # AbstractBaseUser TIDAK memiliki field 'username', jadi hanya periksa 'email'.
        self.assertEqual(user.email, email) 
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.check_password(password))
        
  
