from django.contrib import admin
from .models import User  # Import User model kustom Anda


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Custom configuration for User model in Django Admin."""
    list_display = ['email', 'name', 'is_staff', 'is_superuser']
    search_fields = ['email', 'name']
    ordering = ['email']
# Register your models here.
