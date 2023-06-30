from uuid import uuid4

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        user = self.model(
            email=self.normalize_email(email),
            is_active=True,
            is_staff=is_staff,
            is_superuser=is_superuser,
            last_login=timezone.now(),
            registered_at=timezone.now(),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        is_staff = extra_fields.pop("is_staff", False)
        is_superuser = extra_fields.pop("is_superuser", False)
        return self._create_user(
            email, password, is_staff, is_superuser, **extra_fields
        )

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(
            email, password, is_staff=True, is_superuser=True, **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="Email", unique=True, max_length=255)
    first_name = models.CharField(
        verbose_name="First name", max_length=30, default="first"
    )
    last_name = models.CharField(
        verbose_name="Last name", max_length=30, default="last"
    )
    is_admin = models.BooleanField(verbose_name="Admin", default=False)
    is_active = models.BooleanField(verbose_name="Active", default=True)
    is_staff = models.BooleanField(verbose_name="Staff", default=False)
    registered_at = models.DateTimeField(
        verbose_name="Registered at", auto_now_add=timezone.now
    )
    password_reset_token = models.CharField(blank=True, null=True, max_length=255)
    password_token_created_at = models.DateTimeField(blank=True, null=True)

    # Fields settings
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    full_name.fget.short_description = "Full name"

    @property
    def short_name(self):
        return f"{self.last_name} {self.first_name[0]}."

    short_name.fget.short_description = "Short name"

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.short_name

    def set_password_reset_token(self):
        self.password_reset_token = uuid4()
        self.password_token_created_at = timezone.now()
        self.save()

    def clear_password_reset_token(self):
        self.password_reset_token = None
        self.password_token_created_at = None
        self.save()

    def __str__(self):
        return self.full_name
