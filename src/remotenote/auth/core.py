"""
API Authentication Functions
"""
from __future__ import annotations

from datetime import datetime, timedelta
import logging
import os
from typing import Literal

from jose import jwt
from passlib.context import CryptContext

from .models import UserInDB


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


# to get a string like this run:
# openssl rand -hex 32
# TODO: get secret from the docker container instead of env var
SECRET_KEY = "REMOTENOTE_SAUZ"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(user_db, username: str) -> UserInDB | None:
    if username in user_db:
        user_dict = user_db[username]
        return UserInDB(**user_dict)
    return None


def authenticate_user(
    fake_db, username: str,
    password: str
) -> UserInDB | Literal[False]:
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(
        data: dict,
        expires_delta: timedelta | None = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        get_secret(),
        algorithm=ALGORITHM
    )
    return encoded_jwt


def get_secret():
    logging.critical("API SECRET SHOULD NOT BE STORE AS ENVIRONMENT VAR")
    key = os.getenv(SECRET_KEY, None)
    if key is None:
        raise KeyError("Failed to find the SECRET_SAUZ")
    return key
