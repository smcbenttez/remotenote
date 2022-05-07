"""
FastAPI Router for Users
"""
from fastapi import APIRouter, Depends

from ..dependencies import get_current_user
from ..models import User


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={401: {"description": "Incorrect username or password"}}
)


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
