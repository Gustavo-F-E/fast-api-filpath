from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..crud import create_liner, get_user_liners, update_liner, delete_liner
from ..schemas import LinerCreate, LinerResponse, UserResponse, LinerUpdate
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

@router.put("/{liner_id}", response_model=bool)
async def update_existing_liner(
    liner_id: str,
    liner_data: LinerUpdate,
    current_user: UserResponse = Depends(get_current_user)
):
    """Actualizar liner específico"""
    success = await update_liner(liner_id, current_user.email, liner_data)
    if not success:
        raise HTTPException(status_code=404, detail="Liner no encontrado o no autorizado")
    return success

@router.delete("/{liner_id}", response_model=bool)
async def delete_existing_liner(
    liner_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """Eliminar liner específico"""
    success = await delete_liner(liner_id, current_user.email)
    if not success:
        raise HTTPException(status_code=404, detail="Liner no encontrado o no autorizado")
    return success
