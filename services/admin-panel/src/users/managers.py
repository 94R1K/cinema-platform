from uuid import UUID

from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def sync_from_auth(
        self,
        *,
        user_id: UUID,
        login: str,
        first_name: str,
        last_name: str,
        is_active: bool,
        is_admin: bool,
    ):
        user, created = self.update_or_create(
            id=user_id,
            defaults={
                "login": login,
                "first_name": first_name,
                "last_name": last_name,
                "is_active": is_active,
                "is_admin": is_admin,
            },
        )

        if created:
            user.set_unusable_password()
            user.save(update_fields=["password"])

        return user

    def create_user(self, *args, **kwargs):
        raise NotImplementedError("Users must be created through Auth Service.")

    def create_superuser(self, *args, **kwargs):
        raise NotImplementedError("Users must be created through Auth Service.")
