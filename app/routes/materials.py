from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..crud import create_material, get_user_materials, delete_material
from ..schemas import MaterialCreate, MaterialResponse, UserResponse
from .auth import get_current_user

router = APIRouter(prefix="/materials", tags=["materials"])

@router.get("/", response_model=List[MaterialResponse])
async def read_materials(current_user: UserResponse = Depends(get_current_user)):
    """Obtener materiales del usuario actual"""
    return await get_user_materials(current_user.email)

@router.post("/", response_model=MaterialResponse)
async def create_new_material(
    material: MaterialCreate,
    current_user: UserResponse = Depends(get_current_user)
):
    """Crear o actualizar material"""
    return await create_material(material, current_user.email)

@router.delete("/{material_id}")
async def remove_material(
    material_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """Eliminar un material"""
    success = await delete_material(material_id, current_user.email)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material no encontrado o no autorizado"
        )
    return {"detail": "Material eliminado correctamente"}
