from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from bson import ObjectId

from ..crud import (
    create_project, 
    get_user_projects, 
    get_project_by_id,
    update_project,
    delete_project
)
from ..schemas import ProjectCreate, ProjectUpdate, ProjectResponse, UserResponse
from .auth import get_current_user

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("/", response_model=List[ProjectResponse])
async def read_projects(
    skip: int = 0,
    limit: int = 100,
    current_user: UserResponse = Depends(get_current_user)
):
    """Obtener proyectos del usuario actual"""
    projects = await get_user_projects(current_user.email, skip, limit)
    return projects


@router.post("/", response_model=ProjectResponse)
async def create_new_project(
    project: ProjectCreate,
    current_user: UserResponse = Depends(get_current_user)
):
    created_project = await create_project(project, current_user.email)
    return created_project


@router.get("/{project_id}", response_model=ProjectResponse)
async def read_project(
    project_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    project = await get_project_by_id(project_id)

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Proyecto no encontrado"
        )

    # Validar propiedad del proyecto
    if project["user_email"] != current_user.email:
        raise HTTPException(
            status_code=403,
            detail="No tienes acceso a este proyecto"
        )

    return project


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project_data(
    project_id: str,
    project_update: ProjectUpdate,
    current_user: UserResponse = Depends(get_current_user)
):
    """Actualizar proyecto"""
    updated = await update_project(project_id, current_user.email, project_update)
    
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado o no tienes permisos"
        )
    
    project = await get_project_by_id(project_id)
    return project


@router.delete("/{project_id}")
async def delete_project_data(
    project_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """Eliminar proyecto"""
    deleted = await delete_project(project_id, current_user.email)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado o no tienes permisos"
        )
    
    return {"message": "Proyecto eliminado correctamente"}