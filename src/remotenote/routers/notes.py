"""
FastAPI Router for Notes
"""
from fastapi import APIRouter, Security

from ..auth.dependencies import get_current_active_user
from ..auth.models import User


router = APIRouter(
    prefix="/notes",
    tags=["notes"]
)


@router.get("/")
async def read_items(
    current_user: User = Security(
        get_current_active_user, scopes=["notes"]
    )
):
    return
