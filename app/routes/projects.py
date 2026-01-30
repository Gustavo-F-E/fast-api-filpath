from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from bson import ObjectId

from ..crud import (
    create_project, 
    get_user_projects, 
    get_project_by_id,
    update_project,
    delete_project,
    add_project_layer,
    update_project_layer,
    delete_project_layer
)
from ..schemas import ProjectCreate, ProjectUpdate, ProjectResponse, UserResponse, LayerCreate, LayerUpdate, LayerResponse
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

# ============================================================
#                       RUTAS DE CAPAS (LAYERS)
# ============================================================

@router.post("/{project_id}/layers/", response_model=LayerResponse)
async def create_layer(
    project_id: str,
    layer: LayerCreate,
    current_user: UserResponse = Depends(get_current_user)
):
    """Añadir una capa al proyecto"""
    created_layer = await add_project_layer(project_id, current_user.email, layer)
    if not created_layer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    return created_layer

@router.put("/{project_id}/layers/{layer_id}")
async def update_layer(
    project_id: str,
    layer_id: str,
    layer_update: LayerUpdate,
    current_user: UserResponse = Depends(get_current_user)
):
    """Actualizar una capa del proyecto"""
    updated = await update_project_layer(project_id, layer_id, current_user.email, layer_update)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Capa o proyecto no encontrado"
        )
    return {"message": "Capa actualizada correctamente"}

@router.delete("/{project_id}/layers/{layer_id}")
async def delete_layer(
    project_id: str,
    layer_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """Eliminar una capa del proyecto"""
    deleted = await delete_project_layer(project_id, layer_id, current_user.email)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Capa o proyecto no encontrado"
        )
    return {"message": "Capa eliminada correctamente"}
