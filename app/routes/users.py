# app/routes/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from bson import ObjectId

from ..crud import get_user_by_id, update_user, delete_user
from ..schemas import UserResponse, UserUpdate
from .auth import get_current_user
from ..database import get_users_collection  # Importar la función

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserResponse])
async def read_users():
    """Obtener todos los usuarios (solo admin en producción)"""
    # 🔴 CAMBIA ESTA LÍNEA:
    # users_collection = get_users_collection()  # ❌ ANTES (sin await)
    
    users_collection = await get_users_collection()  # ✅ AHORA (con await)
    
    users = await users_collection.find().to_list(100)
    
    for user in users:
        user["_id"] = str(user["_id"])
    
    return users

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: str):
    """Obtener usuario por ID"""
    user = await get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user_data(
    user_id: str,
    update_data: UserUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Actualizar usuario"""
    # Verificar que el usuario solo se pueda actualizar a sí mismo
    if current_user.id != user_id:  # 🔴 Cambia "_id" por "id"
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No puedes actualizar otros usuarios"
        )
    
    updated = await update_user(user_id, update_data.dict(exclude_unset=True))
    
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Retornar usuario actualizado
    user = await get_user_by_id(user_id)
    return user

@router.delete("/{user_id}")
async def delete_user_data(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Eliminar usuario y TODOS sus proyectos"""
    # Verificar que el usuario solo se pueda eliminar a sí mismo
    if current_user.id != user_id:  # 🔴 Cambia "_id" por "id"
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No puedes eliminar otros usuarios"
        )
    
    deleted = await delete_user(user_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return {"message": "Usuario y todos sus proyectos eliminados correctamente"}