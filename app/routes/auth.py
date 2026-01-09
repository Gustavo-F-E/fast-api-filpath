# app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Header, BackgroundTasks
from datetime import timedelta, datetime
from typing import Dict

from ..auth import create_access_token, verify_token, blacklist_token, blacklist_all_user_tokens
from ..crud import authenticate_user, create_user, get_user_by_email
from ..schemas import UserCreate, UserLogin, Token, UserResponse

router = APIRouter()

# ============================
# LOGIN (JSON)
# ============================
@router.post("/auth/login", response_model=Token)
async def login(data: UserLogin):
    """Iniciar sesión con JSON"""
    user = await authenticate_user(data.email, data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user["email"]},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user["_id"],
            "email": user["email"],
            "username": user["username"],
            "provider": user.get("provider", "local"),
            "created_at": user["created_at"]
        }
    }

# ============================
# OBTENER USUARIO ACTUAL (MODIFICADA PARA ASYNC)
# ============================
async def get_current_user(authorization: str = Header(None)):
    """Obtener usuario actual desde el header Authorization: Bearer <token>"""

    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token faltante",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization.split(" ")[1]
    email = await verify_token(token)  # 🔴 Ahora es async!

    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido, expirado o sesión cerrada",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await get_user_by_email(email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return UserResponse(
        id=str(user["_id"]),
        email=user["email"],
        username=user["username"],
        provider=user.get("provider", "local"),
        created_at=user["created_at"]
    )

# ============================
# REGISTRO
# ============================
@router.post("/auth/register", response_model=UserResponse)
async def register(user: UserCreate):
    """Registrar nuevo usuario"""
    try:
        created_user = await create_user(user)

        return {
            "id": created_user["_id"],
            "email": created_user["email"],
            "username": created_user["username"],
            "provider": created_user.get("provider", "local"),
            "created_at": created_user["created_at"]
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al registrar usuario: {str(e)}"
        )

# ============================
# PERFIL DEL USUARIO
# ============================
@router.get("/auth/me", response_model=UserResponse)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    """Obtener información del usuario actual"""
    return current_user

# ============================
# LOGOUT/CERRAR SESIÓN
# ============================
@router.post("/auth/logout")
async def logout(
    authorization: str = Header(None),
    current_user: dict = Depends(get_current_user),
    background_tasks: BackgroundTasks = None
):
    """Cerrar sesión del usuario actual"""
    
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token no proporcionado"
        )
    
    token = authorization.split(" ")[1]
    
    # Agregar token a lista negra
    if background_tasks:
        background_tasks.add_task(blacklist_token, token, current_user.email)
    else:
        await blacklist_token(token, current_user.email)  # 🔴 Ahora es async
    
    return {
        "message": "Sesión cerrada exitosamente",
        "user_email": current_user.email,
        "logout_time": datetime.utcnow().isoformat()
    }

# ============================
# LOGOUT DE TODAS LAS SESIONES
# ============================
@router.post("/auth/logout-all")
async def logout_all(
    current_user: dict = Depends(get_current_user),
    background_tasks: BackgroundTasks = None
):
    """Cerrar todas las sesiones del usuario"""
    
    if background_tasks:
        background_tasks.add_task(blacklist_all_user_tokens, current_user.email)
    else:
        await blacklist_all_user_tokens(current_user.email)  # 🔴 Ahora es async
    
    return {
        "message": "Solicitud para cerrar todas las sesiones recibida",
        "user_email": current_user.email,
        "logout_time": datetime.utcnow().isoformat(),
        "note": "Tokens serán invalidados progresivamente"
    }