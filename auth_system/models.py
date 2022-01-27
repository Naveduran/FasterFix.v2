from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

class CustomAccountManager(BaseUserManager):
    ''' Allow to create custom user and superuser'''
    def create_superuser(self, email, user_name, first_name, password, **other):
        ''' Create a superuser '''
        other.setdefault('is_staff', True)
        other.setdefault('is_superuser', True)
        other.setdefault('is_active', True)

        if not other.get('is_staff') or not other.get('is_superuser'):
            raise ValueError('Superuser must have is_staff=True and is_superuser=True')

        return self.create_user(email, user_name, first_name, password, **other)
    

    def create_user(self, email, user_name, first_name, password, **other):
        ''' Create a basic user'''
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, first_name=first_name, **other)
        user.set_password(password)
        user.save()

        return user

    
class User(AbstractBaseUser, PermissionsMixin):
    ''' Custom user model '''
    # User data
    email = models.EmailField(max_length=255, unique=True)
    user_name = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)

    # Not set by user
    is_staff = models.BooleanField(default=False, editable=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Manager
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name']

    def __str__(self):
        return self.user_name