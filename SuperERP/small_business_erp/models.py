from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class BusinessUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('erp_role', 'admin')
        return self.create_user(email, password, **extra_fields)

class BusinessUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    erp_role = models.CharField(max_length=50, default='user')
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = BusinessUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Fix clashes with unique related_name
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='business_users',
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='business_users',
        blank=True,
        help_text='Specific permissions for this user.'
    )

    def __str__(self):
        return self.email
