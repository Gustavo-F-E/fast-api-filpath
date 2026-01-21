# app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Header, BackgroundTasks
from datetime import timedelta, datetime
from typing import Dict

from ..auth import create_access_token, verify_token, blacklist_token, blacklist_all_user_tokens
from ..crud import authenticate_user, create_user, get_user_by_email, get_user_by_provider, create_oauth_user
from ..schemas import UserCreate, UserLogin, Token, UserResponse, OAuthLogin

router = APIRouter()

# Guarda temporalmente los authorization codes ya usados
used_oauth_codes: set[str] = set()

# ============================
# OBTENER USUARIO ACTUAL
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

    # 1. Verificamos token y obtenemos datos
    token_data = await verify_token(token)

    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido, expirado o sesión cerrada",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 2. Buscamos usuario real en Mongo usando email y provider
    from ..crud import get_user_by_email_and_provider
    user = await get_user_by_email_and_provider(token_data["email"], token_data["provider"])

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Convertimos dict → UserResponse
    return UserResponse(
        id=str(user["_id"]),
        email=user["email"],
        username=user["username"],
        provider=user.get("provider", "local"),
        created_at=user["created_at"]
    )


# ============================
# LOGIN (JSON)
# ============================
@router.post("/auth/login", response_model=Token)
async def login(data: UserLogin):
    """Iniciar sesión con email O username"""
    # Determinar qué campo usar para log
    login_identifier = data.email if data.email else data.username
    print(f"🔵 [BACKEND] Intento de login estándar recibido: {login_identifier}")

    # Validación manual
    if not data.email and not data.username:
        print(f"🔴 [BACKEND] Login fallido: Faltan credenciales")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe proporcionar email o username"
        )
    
    # Determinar qué campo usar
    login_input = data.email if data.email else data.username
    
    user = await authenticate_user(login_input, data.password)

    if not user:
        print(f"🔴 [BACKEND] Login fallido: Credenciales inválidas para {login_input}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )

    print(f"🟢 [BACKEND] Login exitoso para usuario ID: {user['_id']}")

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user["email"], "provider": user.get("provider", "email")},
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

@router.get("/auth/session")
async def get_session(current_user: dict = Depends(get_current_user)):
    """Obtener información de la sesión actual"""
    return current_user


# ============================
# REGISTRO
# ============================
@router.post("/auth/register", response_model=UserResponse)
async def register(user: UserCreate):
    """Registrar nuevo usuario"""
    print(f"🔵 [BACKEND] Intento de registro estándar: {user.email} / {user.username}")
    try:
        created_user = await create_user(user)
        print(f"🟢 [BACKEND] Registro exitoso para: {created_user['email']}")

        return {
            "id": created_user["_id"],
            "email": created_user["email"],
            "username": created_user["username"],
            "provider": created_user.get("provider", "local"),
            "created_at": created_user["created_at"]
        }

    except ValueError as e:
        print(f"🔴 [BACKEND] Error validación registro: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print(f"🔴 [BACKEND] Error interno en registro: {e}")
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

@router.post("/auth/oauth", response_model=Token)
async def oauth_login(data: OAuthLogin):
    """
    Login o registro usando OAuth (Google, Microsoft, Apple, etc)
    """

    # 🔐 Protección contra reuso de code OAuth
    if data.code in used_oauth_codes:
        print(f"🟠 [BACKEND] Code OAuth ya usado, bloqueando: {data.code}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authorization code already used"
        )

    # Marcamos el code como usado
    used_oauth_codes.add(data.code)
    print(f"🔵 [BACKEND] Code OAuth registrado como usado: {data.code}")

    # 1. Buscar por provider + provider_id
    user = await get_user_by_provider(data.provider, data.provider_id)

    # 2. Si no existe → crear usuario
    if not user:
        try:
            user = await create_oauth_user(data.dict())
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    # 3. Generar JWT incluyendo el provider
    access_token = create_access_token(
        data={"sub": user["email"], "provider": user["provider"]},
        expires_delta=timedelta(minutes=30)
    )

    print(f"🟢 [BACKEND] OAuth login exitoso para {user['email']} ({data.provider})")

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user["_id"],
            "email": user["email"],
            "username": user["username"],
            "provider": user["provider"],
            "created_at": user["created_at"]
        }
    }

