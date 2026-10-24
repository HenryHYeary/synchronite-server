import hashlib
import secrets

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from synchronite_server.app.db import lookup_by_token_hash

bearer = HTTPBearer()

def new_device_token() -> tuple[str, str]:
    raw = secrets.token_urlsafe(32)
    return raw, hashlib.sha256(raw.encode()).hexdigest()

def current_device(creds: HTTPAuthorizationCredentials = Depends(bearer)):
    token_hash = hashlib.sha256(creds.credentials.encode()).hexdigest()
    device = lookup_by_token_hash(token_hash) # TODO write this function
    if device is None:
        raise HTTPException(status_code=401, detail="Invalid or revoked token")
    return device
