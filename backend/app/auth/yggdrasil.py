"""Yggdrasil authentication backend for Microsoft login flow."""

import json
import base64
import hashlib
import time
import os
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any, List
from urllib.parse import urlencode, quote_plus

from fastapi import Request, HTTPException, Header


@dataclass
class YggdrasilAuthResult:
    """Result of Yggdrasil authentication."""
    access_token: str
    client_token: str
    user_id: str
    expires_in: int
    profile: Dict[str, Any]
    selected_profile: bool
    limited: bool


@dataclass
class AuthlibInjectorHeaders:
    """Authlib-Injector compatible headers."""
    authlib_injector: str
    authlib_injector_client: str


class YggdrasilClient:
    """Yggdrasil authentication using the Yggdrasil protocol."""

    AUTHORIZATION_URL = "https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize"
    TOKEN_URL = "https://login.microsoftonline.com/consumers/oauth2/v2.0/token"
    YGGDRASIL_AUTH_URL = "https://authserver.mojang.com/authenticate"
    YGGDRASIL_VALIDATE_URL = "https://authserver.mojang.com/validatecredentials"

    def __init__(self):
        self.client_id = "prism-hub"
        self.redirect_uris = ["http://localhost:8000/auth/callback"]
        self.scopes = ["openid", "profile", "email"]

    async def get_auth_url(self) -> str:
        """Get the authorization URL for Microsoft login."""
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uris[0],
            "response_mode": "query",
            "scope": " ".join(self.scopes),
            "state": self._generate_state(),
        }
        base_url = self.AUTHORIZATION_URL + "?" + urlencode(params)
        return base_url

    async def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """Exchange authorization code for token using httpx."""
        import httpx
        async with httpx.AsyncClient() as client:
            params = {
                "grant_type": "authorization_code",
                "client_id": self.client_id,
                "code": code,
                "redirect_uri": self.redirect_uris[0],
            }
            resp = await client.post(self.TOKEN_URL, data=params)
            resp.raise_for_status()
            return resp.json()

    async def authenticate_with_yggdrasil(
        self,
        username: str,
        password: str,
        client_token: Optional[str] = None,
    ) -> YggdrasilAuthResult:
        """
        Authenticate with Microsoft/Yggdrasil.
        """
        auth_payload = {
            "username": username,
            "password": password,
            "clientToken": client_token or f"prism-{int(time.time())}",
            "requestUser": True,
        }

        async with httpx.AsyncClient() as client:
            resp = await client.post(self.YGGDRASIL_AUTH_URL, json=auth_payload)
            resp.raise_for_status()
            auth_data = resp.json()

        if auth_data.get("accessToken"):
            validate_payload = {
                "username": username,
                "password": password,
                "clientToken": auth_data.get("clientToken"),
            }
            validate_resp = await client.post(
                self.YGGDRASIL_VALIDATE_URL,
                json=validate_payload,
            )
            validate_resp.raise_for_status()
            validate_data = validate_resp.json()

            return YggdrasilAuthResult(
                access_token=auth_data["accessToken"],
                client_token=auth_data.get("clientToken", client_token or ""),
                user_id=auth_data.get("uuid", ""),
                expires_in=3600,
                profile=auth_data.get("profile", {}),
                selected_profile=auth_data.get("selectedProfile", False),
                limited=auth_data.get("limited", False),
            )
        else:
            raise HTTPException(
                status_code=401,
                detail="Authentication failed: " + str(auth_data.get("error", "unknown error")),
            )

    @staticmethod
    def _generate_state() -> str:
        """Generate a random state parameter for OAuth."""
        return base64.urlsafe_b64encode(os.urandom(32)).decode("utf-8")[:16]


# Global instance
yggdrasil = YggdrasilClient()


def generate_authlib_injector_headers(
    access_token: str,
    client_token: str,
) -> AuthlibInjectorHeaders:
    """
    Generate authlib-injector compatible headers.
    """
    injector_string = (
        f"authlib-injector;"
        f"key={access_token};"
        f"client_token={client_token}"
    )

    return AuthlibInjectorHeaders(
        authlib_injector=injector_string,
        authlib_injector_client=client_token,
    )


def validate_offline_mode(
    client_token: str,
    username: str,
    uuid: str,
) -> bool:
    """
    Validate offline mode authentication.
    """
    name_hash = int(hashlib.sha1(username.encode("utf-8")).hexdigest()[:8], 16)
    generated_uuid = (
        f"00000000-{name_hash % 0x10000:04x}"
        f"-{name_hash % 0x10000:04x}"
        f"-{name_hash % 0x10000:04x}"
        f"-{name_hash % 0x1000000000000:012x}"
    )

    return generated_uuid == uuid and client_token is not None


async def require_authlib_injector(
    request: Request,
    authlib_injector: str = Header(...),
) -> AuthlibInjectorHeaders:
    """
    FastAPI dependency that validates authlib-injector headers.
    """
    try:
        parts = authlib_injector.split(";")
        params = {}
        for part in parts:
            if "=" in part:
                key, value = part.split("=", 1)
                params[key.strip()] = value.strip()

        access_token = params.get("key", "")
        client_token = params.get("client_token", "")

        if not access_token or not client_token:
            raise HTTPException(
                status_code=401,
                detail="Invalid authlib-injector headers: missing key or client_token",
            )

        return AuthlibInjectorHeaders(
            authlib_injector=authlib_injector,
            authlib_injector_client=client_token,
        )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid authlib-injector headers: {str(e)}",
        )
