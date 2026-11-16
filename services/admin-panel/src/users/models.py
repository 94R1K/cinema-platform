from typing import ClassVar

from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from users.managers import UserManager


class User(AbstractBaseUser):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
    )
    login = models.CharField(
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "login"
    REQUIRED_FIELDS: ClassVar[list[str]] = []

    class Meta:
        db_table = "admin_users"

    @property
    def is_staff(self) -> bool:
        return self.is_active and self.is_admin

    def has_perm(self, _perm, _obj=None) -> bool:
        return self.is_staff

    def has_module_perms(self, _app_label) -> bool:
        return self.is_staff

    def __str__(self) -> str:
        return self.login
