from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..crud import create_liner, get_user_liners
from ..schemas import LinerCreate, LinerResponse, UserResponse
from .auth import get_current_user

router = APIRouter(prefix="/liners", tags=["liners"])

@router.get("/", response_model=List[LinerResponse])
async def read_liners(current_user: UserResponse = Depends(get_current_user)):
    """Obtener liners del usuario actual"""
    return await get_user_liners(current_user.email)

@router.post("/", response_model=LinerResponse)
async def create_new_liner(
    liner: LinerCreate,
    current_user: UserResponse = Depends(get_current_user)
):
    """Crear o actualizar liner"""
    return await create_liner(liner, current_user.email)
