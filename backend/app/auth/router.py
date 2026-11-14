"""Yggdrasil authentication API routes."""

from fastapi import APIRouter, Depends, Request, Header, HTTPException
from typing import Dict, Any
from authlib.integrations.starlette_client import OAuth

from app.auth.yggdrasil import (
    yggdrasil,
    YggdrasilAuthResult,
    AuthlibInjectorHeaders,
    generate_authlib_injector_headers,
    validate_offline_mode,
    require_authlib_injector,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/yggdrasil/login")
async def yggdrasil_login(request: Request):
    """Initiate Microsoft/Yggdrasil OAuth login flow."""
    auth_url = await yggdrasil.get_auth_url()
    return {"auth_url": auth_url, "message": "Visit this URL to login with Microsoft account"}


@router.get("/yggdrasil/callback")
async def yggdrasil_callback(request: Request):
    """Handle Microsoft/Yggdrasil OAuth callback."""
    code = request.query_params.get("code")
    state = request.query_params.get("state")
    
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")
    
    token_data = await yggdrasil.exchange_code_for_token(code)
    client_token = token_data.get("access_token", "")
    
    headers = generate_authlib_injector_headers(
        access_token=client_token,
        client_token=client_token,
    )
    
    return {
        "access_token": client_token,
        "client_token": client_token,
        "authlib_injector_headers": {"authlib_injector": headers.authlib_injector, "authlib_injector_client": headers.authlib_injector_client},
        "message": "Yggdrasil authentication successful",
    }


@router.post("/yggdrasil/login-direct")
async def yggdrasil_login_direct(
    username: str, password: str, client_token: str = None,
) -> YggdrasilAuthResult:
    """Direct Microsoft/Yggdrasil authentication."""
    result = await yggdrasil.authenticate_with_yggdrasil(username=username, password=password, client_token=client_token)
    return result


@router.post("/yggdrasil/offline")
async def yggdrasil_offline(username: str, uuid: str, client_token: str) -> Dict[str, Any]:
    """Offline mode authentication."""
    import hashlib
    name_hash = int(hashlib.sha1(username.encode()).hexdigest()[:8], 16)
    generated_uuid = f"00000000-{name_hash % 0x10000:04x}-{name_hash % 0x10000:04x}-{name_hash % 0x10000:04x}-{name_hash % 0x1000000000000:012x}"
    is_valid = generated_uuid == uuid and client_token is not None
    
    if not is_valid:
        raise HTTPException(status_code=401, detail="Invalid offline authentication")
    
    headers = generate_authlib_injector_headers(access_token="", client_token=client_token)
    
    return {"authenticated": True, "mode": "offline", "username": username, "client_token": client_token, "authlib_injector": headers.authlib_injector}


@router.post("/injector/headers")
async def get_injector_headers(auth: AuthlibInjectorHeaders = Depends(require_authlib_injector)) -> Dict[str, str]:
    return {"Authorization": f"Bearer {auth.authlib_injector_client}", "Authlib-Injector": auth.authlib_injector}
