"""
Database models
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group,          # Required for ManyToManyField definition
    Permission      # Required for ManyToManyField definition
)


class UserManager(BaseUserManager):
    """Manager for custom User model."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new User."""
        if not email:
            raise ValueError('Users must have an email address')
            
        # 🎯 FIX NORMALIZATION: Memastikan email dinormalisasi di sini sebelum disimpan
        # BaseUserManager.normalize_email() akan menormalkan bagian domain dan nama pengguna.
        email = email.lower()
        email = self.normalize_email(email)
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a new superuser with given details."""
        # 🎯 FIX SUPERUSER ARGUMENTS: Metode ini sekarang menerima **extra_fields
        # untuk mengatasi TypeError saat argumen REQUIRED_FIELDS (seperti 'name') diteruskan.
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        # Validation checks (recommended practice)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Call the create_user method to handle normalization and password hashing
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User in the system using email as the unique identifier."""
    
    # Core Fields
    
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    
    # ----------------------------------------------------
    # FIX: OVERRIDING PERMISSIONS MIXIN FIELDS TO AVOID RELATED_NAME CLASH
    # ----------------------------------------------------
    
    # 1. Overriding 'groups' field
    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="core_user_groups", 
    )
    
    # 2. Overriding 'user_permissions' field
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="core_user_permissions_set", 
    )
    # ----------------------------------------------------
    
    
    # Manager and Identifier settings
    objects = UserManager() 
    
    # Tells Django to use the 'email' field for logging in
    USERNAME_FIELD = "email" 
    
    # Fields that will be requested when creating a user via 'createsuperuser'
    REQUIRED_FIELDS = ['name'] 

    def __str__(self):
        return self.email
