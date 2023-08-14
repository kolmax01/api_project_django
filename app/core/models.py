from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin # noqa


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **some_extra_fields_if_needed):
        if not email:
            raise ValueError('Email address is required')
        user = self.model(email=self.normalize_email(email),
                          **some_extra_fields_if_needed)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class NnModels(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    used_for = models.CharField(max_length=50)
    model_size = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
