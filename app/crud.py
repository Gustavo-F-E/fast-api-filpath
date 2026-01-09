# app/crud.py - VERSIÓN CORREGIDA
from typing import Optional
from bson import ObjectId
from datetime import datetime
from .database import get_users_collection, get_projects_collection  # Estas son async ahora
from .auth import get_password_hash, verify_password
from .schemas import UserCreate, UserLogin, ProjectCreate, ProjectUpdate
import logging

logger = logging.getLogger(__name__)

# ============================================================
#                       CRUD USUARIOS
# ============================================================

async def create_user(user: UserCreate):
    """Crear nuevo usuario"""
    users_collection = await get_users_collection()  # 🔴 AGREGAR AWAIT

    # Verificar si el usuario ya existe
    existing_user = await users_collection.find_one({
        "$or": [
            {"email": user.email},
            {"username": user.username}
        ]
    })

    if existing_user:
        raise ValueError("Email o username ya registrado")

    # Crear usuario
    user_dict = user.dict()
    user_dict["password_hash"] = get_password_hash(user.password)
    del user_dict["password"]

    user_dict["created_at"] = datetime.utcnow()
    user_dict["updated_at"] = datetime.utcnow()

    result = await users_collection.insert_one(user_dict)

    # Retornar usuario creado
    created_user = await users_collection.find_one({"_id": result.inserted_id})
    created_user["_id"] = str(created_user["_id"])

    return created_user


async def authenticate_user(email: str, password: str):
    """Autenticar usuario"""
    users_collection = await get_users_collection()  # 🔴 AGREGAR AWAIT

    user = await users_collection.find_one({"email": email})

    if not user:
        return None

    if not user.get("password_hash"):
        raise ValueError("Usuario registrado con OAuth, usa método social")

    if not verify_password(password, user["password_hash"]):
        return None

    user["_id"] = str(user["_id"])
    return user


async def get_user_by_id(user_id: str):
    """Obtener usuario por ID"""
    users_collection = await get_users_collection()  # 🔴 AGREGAR AWAIT

    try:
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            user["_id"] = str(user["_id"])
        return user
    except:
        return None


async def get_user_by_email(email: str):
    """Obtener usuario por email"""
    users_collection = await get_users_collection()  # 🔴 AGREGAR AWAIT

    user = await users_collection.find_one({"email": email})
    if user:
        user["_id"] = str(user["_id"])
    return user


async def update_user(user_id: str, update_data: dict):
    """Actualizar usuario"""
    users_collection = await get_users_collection()  # 🔴 AGREGAR AWAIT

    update_data["updated_at"] = datetime.utcnow()

    result = await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data}
    )

    return result.modified_count > 0


async def delete_user(user_id: str):
    """Eliminar usuario y TODOS sus proyectos"""
    users_collection = await get_users_collection()  # 🔴 AGREGAR AWAIT
    projects_collection = await get_projects_collection()  # 🔴 AGREGAR AWAIT

    # Obtener usuario para saber su email
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        return False

    email = user["email"]

    # Eliminar proyectos asociados al email
    delete_projects_result = await projects_collection.delete_many(
        {"user_email": email}
    )

    logger.info(f"Eliminados {delete_projects_result.deleted_count} proyectos del usuario {email}")

    # Eliminar usuario
    delete_user_result = await users_collection.delete_one(
        {"_id": ObjectId(user_id)}
    )

    return delete_user_result.deleted_count > 0


# ============================================================
#                       CRUD PROYECTOS
# ============================================================

async def create_project(project: ProjectCreate, user_email: str):
    projects_collection = await get_projects_collection()  # 🔴 AGREGAR AWAIT

    project_dict = project.dict()
    project_dict["user_email"] = user_email
    project_dict["created_at"] = datetime.utcnow()
    project_dict["updated_at"] = datetime.utcnow()

    result = await projects_collection.insert_one(project_dict)

    created_project = await projects_collection.find_one({"_id": result.inserted_id})
    created_project["_id"] = str(created_project["_id"])

    return created_project


async def get_user_projects(user_email: str, skip: int = 0, limit: int = 100):
    """Obtener proyectos de un usuario por email"""
    projects_collection = await get_projects_collection()  # 🔴 AGREGAR AWAIT

    projects = await projects_collection.find(
        {"user_email": user_email}
    ).sort("created_at", -1).skip(skip).limit(limit).to_list(length=limit)

    for project in projects:
        project["_id"] = str(project["_id"])

    return projects


async def get_project_by_id(project_id: str):
    """Obtener proyecto por ID"""
    projects_collection = await get_projects_collection()  # 🔴 AGREGAR AWAIT

    try:
        project = await projects_collection.find_one({"_id": ObjectId(project_id)})
        if project:
            project["_id"] = str(project["_id"])
        return project
    except:
        return None


async def update_project(project_id: str, user_email: str, update_data: ProjectUpdate):
    """Actualizar proyecto"""
    projects_collection = await get_projects_collection()  # 🔴 AGREGAR AWAIT

    update_dict = update_data.dict(exclude_unset=True)
    update_dict["updated_at"] = datetime.utcnow()

    result = await projects_collection.update_one(
        {"_id": ObjectId(project_id), "user_email": user_email},
        {"$set": update_dict}
    )

    return result.modified_count > 0


async def delete_project(project_id: str, user_email: str):
    """Eliminar proyecto"""
    projects_collection = await get_projects_collection()  # 🔴 AGREGAR AWAIT

    result = await projects_collection.delete_one(
        {"_id": ObjectId(project_id), "user_email": user_email}
    )

    return result.deleted_count > 0