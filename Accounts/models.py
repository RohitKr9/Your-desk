from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self, email, password=None, first_name='', last_name='', **extra_fields):
        if not email:
            raise ValueError("Email is mandatory to provide")
        
        _email = self.normalize_email(email)
        user = self.model(email = _email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, email, password = None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser",True)

        return self.create_user(email, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'


