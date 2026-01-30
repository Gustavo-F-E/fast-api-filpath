from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..crud import create_machine, get_user_machines, update_machine, delete_machine
from ..schemas import MachineCreate, MachineResponse, UserResponse, MachineUpdate
from .auth import get_current_user

router = APIRouter(prefix="/machines", tags=["machines"])

@router.get("/", response_model=List[MachineResponse])
async def read_machines(current_user: UserResponse = Depends(get_current_user)):
    """Obtener máquinas del usuario actual"""
    return await get_user_machines(current_user.email)

@router.post("/", response_model=MachineResponse)
async def create_new_machine(
    machine: MachineCreate,
    current_user: UserResponse = Depends(get_current_user)
):
    """Crear o actualizar máquina"""
    return await create_machine(machine, current_user.email)

@router.put("/{machine_id}", response_model=bool)
async def update_existing_machine(
    machine_id: str,
    machine_data: MachineUpdate,
    current_user: UserResponse = Depends(get_current_user)
):
    """Actualizar máquina específica"""
    success = await update_machine(machine_id, current_user.email, machine_data)
    if not success:
        raise HTTPException(status_code=404, detail="Máquina no encontrada o no autorizada")
    return success

@router.delete("/{machine_id}", response_model=bool)
async def delete_existing_machine(
    machine_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """Eliminar máquina específica"""
    success = await delete_machine(machine_id, current_user.email)
    if not success:
        raise HTTPException(status_code=404, detail="Máquina no encontrada o no autorizada")
    return success
