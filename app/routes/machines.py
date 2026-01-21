from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..crud import create_machine, get_user_machines
from ..schemas import MachineCreate, MachineResponse, UserResponse
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
