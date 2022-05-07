"""
FastAPI Dependencies for Authentication
"""
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from pydantic import ValidationError

from .core import ALGORITHM, fake_users_db, get_secret, get_user
from .models import User, TokenData


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth",
    scopes={
        "me": "Read information about the current user.",
        "notes": "Read and write notes."
    }
)


async def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme)
):
    authenticate_value = "Bearer"
    if security_scopes.scopes:
        authenticate_value += f" scope={security_scopes.scope_str}"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, get_secret(), algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    # mypy doesn't recognize the unwrapping in the try block
    user = get_user(
        fake_users_db,
        username=token_data.username  # type: ignore
    )
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value}
            )
    return user


async def get_current_active_user(
    current_user: User = Security(get_current_user, scopes=["me"])
):
    if current_user.disabled:
        raise HTTPException(
            status_code=400,
            detail="Inactive User"
        )
    return current_user
