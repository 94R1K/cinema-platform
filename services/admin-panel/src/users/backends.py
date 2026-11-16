from uuid import UUID, uuid4

from django.contrib.auth.backends import BaseBackend
from django.core.exceptions import ValidationError

from users.clients.auth import AuthServiceClient
from users.exceptions import AuthServiceUnavailable
from users.models import User
from users.roles import Roles


class AuthServiceBackend(BaseBackend):
    def authenticate(
        self,
        request,
        username: str | None = None,
        password: str | None = None,
        **kwargs,
    ) -> User | None:
        login = kwargs.get("login") or username

        if not login or not password:
            return None

        request_id = (
            request.headers.get("X-Request-Id") if request is not None else None
        )

        data = AuthServiceClient.authenticate(
            login=login,
            password=password,
            request_id=request_id or str(uuid4()),
        )

        if data is None:
            return None

        try:
            user_data = data["user"]

            if not isinstance(user_data, dict):
                raise TypeError("User data must be an object.")

            user_id = user_data["id"]
            user_login = user_data["login"]
            is_active = user_data["is_active"]
            roles = user_data["roles"]

            if not isinstance(user_id, str):
                raise TypeError("User ID must be a string.")

            if not isinstance(user_login, str):
                raise TypeError("User login must be a string.")

            if not isinstance(is_active, bool):
                raise TypeError("is_active must be a boolean.")

            if not isinstance(roles, list) or not all(
                isinstance(role, str) for role in roles
            ):
                raise TypeError("User roles must be a list of strings.")

            user_id = UUID(user_id)

        except (KeyError, TypeError, ValueError) as exc:
            raise AuthServiceUnavailable(
                "Invalid user data from Auth Service."
            ) from exc

        is_admin = Roles.ADMIN.value in roles

        if not is_active or not is_admin:
            return None

        return User.objects.sync_from_auth(
            user_id=user_id,
            login=user_login,
            first_name=user_data.get("first_name") or "",
            last_name=user_data.get("last_name") or "",
            is_active=is_active,
            is_admin=is_admin,
        )

    def get_user(self, user_id: str) -> User | None:
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist, ValueError, ValidationError:
            return None

        if not user.is_active or not user.is_admin:
            return None

        return user
