# app/crud.py - VERSIÓN CORREGIDA
from typing import Optional
from bson import ObjectId
from datetime import datetime
from .database import get_users_collection, get_projects_collection, get_liners_collection, get_machines_collection, get_materials_collection  # Estas son async ahora
from .auth import get_password_hash, verify_password
from .schemas import UserCreate, UserLogin, ProjectCreate, ProjectUpdate, LinerCreate, MachineCreate, LinerUpdate, MachineUpdate, LayerCreate, LayerUpdate, MaterialCreate, MaterialUpdate
import logging

logger = logging.getLogger(__name__)

# ============================================================
#                       CRUD USUARIOS
# ============================================================

async def create_user(user: UserCreate):
    """Crear nuevo usuario"""
    users_collection = await get_users_collection()  # 🔴 AGREGAR AWAIT

    # Verificar si el usuario ya existe para este proveedor
    existing_user = await users_collection.find_one({
        "$and": [
            {"provider": user.provider},
            {
                "$or": [
                    {"email": user.email},
                    {"username": user.username}
                ]
            }
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


async def authenticate_user(login_input: str, password: str):
    """Autenticar usuario por email O username"""
    users_collection = await get_users_collection()

    # Determinar si es email o username
    is_email = "@" in login_input
    
    if is_email:
        user = await users_collection.find_one({
            "email": login_input, 
            "$or": [{"provider": "email"}, {"provider": {"$exists": False}}]
        })
    else:
        user = await users_collection.find_one({
            "username": login_input, 
            "$or": [{"provider": "email"}, {"provider": {"$exists": False}}]
        })

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
    """Obtener usuario por email (devuelve el primero que encuentre, usar con precaución)"""
    users_collection = await get_users_collection()

    user = await users_collection.find_one({"email": email})
    if user:
        user["_id"] = str(user["_id"])
    return user


async def get_user_by_email_and_provider(email: str, provider: str):
    """Obtener usuario por email y proveedor específico"""
    users_collection = await get_users_collection()

    user = await users_collection.find_one({"email": email, "provider": provider})
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
#                       HELPERS
# ============================================================

def calculate_project_completion(project_dict: dict) -> int:
    """Calcular el porcentaje de finalización de un proyecto"""
    percentage = 0
    
    # Descripción: 10%
    if project_dict.get("description"):
        percentage += 10
        
    # Liner: 30% (Total 40%)
    if project_dict.get("liner_name"):
        percentage += 30
        
    # Máquina: 30% (Total 70%)
    if project_dict.get("machine_name"):
        percentage += 30
        
    # Capas: 30% (Total 100%)
    if project_dict.get("layers") and len(project_dict.get("layers")) > 0:
        percentage += 30
        
    return percentage

# ============================================================
#                       CRUD PROYECTOS
# ============================================================

async def create_project(project: ProjectCreate, user_email: str):
    projects_collection = await get_projects_collection()  # 🔴 AGREGAR AWAIT

    project_dict = project.dict()
    project_dict["user_email"] = user_email
    project_dict["completion_percentage"] = calculate_project_completion(project_dict)
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
    
    # Recalcular porcentaje si cambian los campos relevantes
    # Primero obtenemos el proyecto actual para fusionar estados
    current_project = await projects_collection.find_one({"_id": ObjectId(project_id)})
    if current_project:
        temp_dict = {**current_project, **update_dict}
        update_dict["completion_percentage"] = calculate_project_completion(temp_dict)

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

async def get_user_by_provider(provider: str, provider_id: str):
    users_collection = await get_users_collection()
    user = await users_collection.find_one({
        "provider": provider,
        "provider_id": provider_id
    })
    if user:
        user["_id"] = str(user["_id"])
    return user

async def create_oauth_user(data: dict):
    users_collection = await get_users_collection()

    # Buscar si ya existe este usuario para ESTE proveedor específico
    existing_user = await users_collection.find_one({
        "email": data["email"],
        "provider": data["provider"]
    })
    
    if existing_user:
        existing_user["_id"] = str(existing_user["_id"])
        return existing_user

    user_dict = {
        "email": data["email"],
        "username": data["username"],
        "provider": data["provider"],
        "provider_id": data["provider_id"],
        "password_hash": None,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }

    result = await users_collection.insert_one(user_dict)
    user = await users_collection.find_one({"_id": result.inserted_id})
    user["_id"] = str(user["_id"])
    return user

# ============================================================
#                       CRUD LINERS
# ============================================================

async def create_liner(liner: LinerCreate, user_email: str):
    liners_collection = await get_liners_collection()
    liner_dict = liner.dict()
    liner_dict["user_email"] = user_email
    liner_dict["created_at"] = datetime.utcnow()
    liner_dict["updated_at"] = datetime.utcnow()
    
    # Evitar duplicados por nombre para el mismo usuario
    await liners_collection.delete_many({"name": liner.name, "user_email": user_email})
    
    result = await liners_collection.insert_one(liner_dict)
    created = await liners_collection.find_one({"_id": result.inserted_id})
    created["_id"] = str(created["_id"])
    return created

async def get_user_liners(user_email: str):
    liners_collection = await get_liners_collection()
    liners = await liners_collection.find({"user_email": user_email}).to_list(length=100)
    for l in liners:
        l["_id"] = str(l["_id"])
    return liners

async def update_liner(liner_id: str, user_email: str, update_data: LinerUpdate):
    liners_collection = await get_liners_collection()
    update_dict = update_data.dict(exclude_unset=True)
    update_dict["updated_at"] = datetime.utcnow()
    
    result = await liners_collection.update_one(
        {"_id": ObjectId(liner_id), "user_email": user_email},
        {"$set": update_dict}
    )
    return result.modified_count > 0

async def delete_liner(liner_id: str, user_email: str):
    liners_collection = await get_liners_collection()
    result = await liners_collection.delete_one(
        {"_id": ObjectId(liner_id), "user_email": user_email}
    )
    return result.deleted_count > 0

# ============================================================
#                       CRUD MAQUINAS
# ============================================================

async def create_machine(machine: MachineCreate, user_email: str):
    machines_collection = await get_machines_collection()
    machine_dict = machine.dict()
    machine_dict["user_email"] = user_email
    machine_dict["created_at"] = datetime.utcnow()
    machine_dict["updated_at"] = datetime.utcnow()
    
    # Evitar duplicados por nombre para el mismo usuario
    await machines_collection.delete_many({"name": machine.name, "user_email": user_email})
    
    result = await machines_collection.insert_one(machine_dict)
    created = await machines_collection.find_one({"_id": result.inserted_id})
    created["_id"] = str(created["_id"])
    return created

async def get_user_machines(user_email: str):
    machines_collection = await get_machines_collection()
    machines = await machines_collection.find({"user_email": user_email}).to_list(length=100)
    for m in machines:
        m["_id"] = str(m["_id"])
    return machines

async def update_machine(machine_id: str, user_email: str, update_data: MachineUpdate):
    machines_collection = await get_machines_collection()
    update_dict = update_data.dict(exclude_unset=True)
    update_dict["updated_at"] = datetime.utcnow()
    
    result = await machines_collection.update_one(
        {"_id": ObjectId(machine_id), "user_email": user_email},
        {"$set": update_dict}
    )
    return result.modified_count > 0

async def delete_machine(machine_id: str, user_email: str):
    machines_collection = await get_machines_collection()
    result = await machines_collection.delete_one(
        {"_id": ObjectId(machine_id), "user_email": user_email}
    )
    return result.deleted_count > 0

# ============================================================
#                       CRUD CAPAS (LAYERS)
# ============================================================

async def add_project_layer(project_id: str, user_email: str, layer: LayerCreate):
    """Añadir una capa a un proyecto"""
    projects_collection = await get_projects_collection()
    
    layer_dict = layer.dict()
    layer_dict["id"] = str(ObjectId())
    
    # Obtener el proyecto actual para recalcular progreso
    project = await projects_collection.find_one({"_id": ObjectId(project_id), "user_email": user_email})
    if not project:
        return None
        
    layers = project.get("layers", [])
    layers.append(layer_dict)
    
    # Recalcular progreso
    completion = calculate_project_completion({**project, "layers": layers})
    
    await projects_collection.update_one(
        {"_id": ObjectId(project_id), "user_email": user_email},
        {
            "$set": {
                "layers": layers,
                "completion_percentage": completion,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    return layer_dict

async def update_project_layer(project_id: str, layer_id: str, user_email: str, layer_update: LayerUpdate):
    """Actualizar una capa específica de un proyecto"""
    projects_collection = await get_projects_collection()
    
    project = await projects_collection.find_one({"_id": ObjectId(project_id), "user_email": user_email})
    if not project:
        return None
        
    layers = project.get("layers", [])
    updated = False
    new_layers = []
    
    update_data = layer_update.dict(exclude_unset=True)
    
    for l in layers:
        if l.get("id") == layer_id:
            updated_layer = {**l, **update_data}
            new_layers.append(updated_layer)
            updated = True
        else:
            new_layers.append(l)
            
    if not updated:
        return None
        
    completion = calculate_project_completion({**project, "layers": new_layers})
    
    await projects_collection.update_one(
        {"_id": ObjectId(project_id), "user_email": user_email},
        {
            "$set": {
                "layers": new_layers,
                "completion_percentage": completion,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    return True

async def delete_project_layer(project_id: str, layer_id: str, user_email: str):
    """Eliminar una capa específica de un proyecto"""
    projects_collection = await get_projects_collection()
    
    project = await projects_collection.find_one({"_id": ObjectId(project_id), "user_email": user_email})
    if not project:
        return False
        
    layers = project.get("layers", [])
    new_layers = [l for l in layers if l.get("id") != layer_id]
    
    if len(new_layers) == len(layers):
        return False
        
    completion = calculate_project_completion({**project, "layers": new_layers})
    
    await projects_collection.update_one(
        {"_id": ObjectId(project_id), "user_email": user_email},
        {
            "$set": {
                "layers": new_layers,
                "completion_percentage": completion,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    return True

# ============================================================
#                       CRUD MATERIALES
# ============================================================

async def create_material(material: MaterialCreate, user_email: str):
    """Crear o actualizar material (duplicados por nombre se sobreescriben)"""
    materials_collection = await get_materials_collection()
    material_dict = material.dict()
    material_dict["user_email"] = user_email
    material_dict["created_at"] = datetime.utcnow()
    material_dict["updated_at"] = datetime.utcnow()
    
    # Evitar duplicados por nombre para el mismo usuario
    await materials_collection.delete_many({"name": material.name, "user_email": user_email})
    
    result = await materials_collection.insert_one(material_dict)
    created = await materials_collection.find_one({"_id": result.inserted_id})
    created["_id"] = str(created["_id"])
    return created

async def get_user_materials(user_email: str):
    """Obtener todos los materiales de un usuario"""
    materials_collection = await get_materials_collection()
    materials = await materials_collection.find({"user_email": user_email}).to_list(length=100)
    for m in materials:
        m["_id"] = str(m["_id"])
    return materials

async def delete_material(material_id: str, user_email: str):
    """Eliminar un material"""
    materials_collection = await get_materials_collection()
    result = await materials_collection.delete_one({"_id": ObjectId(material_id), "user_email": user_email})
    return result.deleted_count > 0
