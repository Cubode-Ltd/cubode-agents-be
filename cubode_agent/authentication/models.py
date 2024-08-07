from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class UserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None):

        if not email:
            raise TypeError("Users should have a email")

        if username is None:
            username = self.generate_username_from_email(email)

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError("Password should not be none")

        user = self.create_user(email, username, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_verified = True
        user.save()
        return user

    def generate_username_from_email(self, email):
        base_username = email.split('@')[0]
        username = base_username
        while User.objects.filter(username=username).exists():
            username = f"{base_username}_{get_random_string(4)}"
        return username


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True)
    slug = models.SlugField(blank=True, null=True)

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_member_pro = models.BooleanField(default=False)
    is_enterprise_member = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        qs = User.objects \
            .filter(slug=self.slug) \
            .exclude(username=self.username)

        if qs.exists():
            self.slug = f"{self.slug}-{qs.count()+1}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
