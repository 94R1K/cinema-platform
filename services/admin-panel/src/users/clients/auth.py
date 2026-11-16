import requests
from django.conf import settings

from users.exceptions import AuthServiceUnavailable


class AuthServiceClient:
    @staticmethod
    def authenticate(
        *,
        login: str,
        password: str,
        request_id: str,
    ) -> dict | None:
        try:
            response = requests.post(
                settings.AUTH_API_LOGIN_URL,
                json={
                    "login": login,
                    "password": password,
                },
                headers={
                    "X-Request-Id": request_id,
                },
                timeout=(3, 5),
            )
        except requests.RequestException as exc:
            raise AuthServiceUnavailable("Cannot connect to Auth Service.") from exc

        if response.status_code in {400, 401, 403}:
            return None

        if response.status_code == 404:
            raise AuthServiceUnavailable(
                f"Auth login endpoint not found: {response.url}"
            )

        if response.status_code == 429 or response.status_code >= 500:
            raise AuthServiceUnavailable(
                f"Auth Service returned HTTP {response.status_code}."
            )

        try:
            response.raise_for_status()
        except requests.RequestException as exc:
            raise AuthServiceUnavailable(
                f"Unexpected HTTP status from Auth Service: {response.status_code}."
            ) from exc

        try:
            data = response.json()
        except ValueError as exc:
            raise AuthServiceUnavailable("Auth Service returned invalid JSON.") from exc

        if not isinstance(data, dict):
            raise AuthServiceUnavailable("Unexpected Auth Service response format.")

        return data
