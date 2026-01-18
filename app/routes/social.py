# app/routes/social.py
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from datetime import timedelta
import os

from ..social_auth import get_google_user, get_github_user, get_microsoft_user, SocialAuthError
from ..crud import get_user_by_email, create_oauth_user, update_user
from ..auth import create_access_token
from ..schemas import Token

router = APIRouter()
# 🔐 Guarda temporalmente los authorization codes ya usados
used_social_codes: set[str] = set()

class SocialLoginRequest(BaseModel):
    provider: str
    code: str
    redirect_uri: str

@router.get("/auth/social/url")
async def get_social_auth_url(provider: str):
    """
    Devuelve la URL para redirigir al usuario al proveedor de OAuth.
    """
    print(f"\n🚀 [OAuth Debug] Generando URL para provider: {provider}")
    
    frontend_url = os.getenv("URL_FRONTEND", "http://localhost:3000").rstrip('/')
    print(f"   - URL_FRONTEND configurada: {frontend_url}")
    if provider == "google":
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        redirect_uri = os.getenv("GOOGLE_REDIRECT_URI", f"{frontend_url}/auth/callback/google")
        scope = "openid email profile"
        return {
            "url": f"https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&access_type=offline"
        }
    elif provider == "github":
        client_id = os.getenv("GITHUB_CLIENT_ID")
        redirect_uri = os.getenv("GITHUB_REDIRECT_URI", f"{frontend_url}/auth/callback/github")
        print(f"   - [GitHub Debug] Redirect URI que se enviará a GitHub: {redirect_uri}")
        url = f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=user:email"
        return {"url": url}
    elif provider == "microsoft":
        client_id = os.getenv("MICROSOFT_CLIENT_ID")
        redirect_uri = os.getenv("MICROSOFT_REDIRECT_URI", f"{frontend_url}/auth/callback/microsoft")
        scope = "User.Read email openid profile"
        return {
            "url": f"https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&response_mode=query&scope={scope}"
        }
    
    print(f"🔴 [BACKEND] Proveedor no soportado: {provider}")
    raise HTTPException(status_code=400, detail="Proveedor no soportado")

@router.post("/auth/social/login", response_model=Token)
async def social_login(data: SocialLoginRequest):
    """
    Login estándar para redes sociales via Authorization Code Flow.
    Recibe el 'code' del frontend, lo valida en el backend y devuelve JWT.
    """

    print(f"\n📥 [OAuth Debug] Social Login POST recibido")
    print(f"   - Provider: {data.provider}")
    print(f"   - Redirect URI recibida: {data.redirect_uri}")
    print(f"   - Code recibido (truncado): {data.code[:10]}...")

    # 🔐 BLOQUEO CONTRA REUSO DEL CODE
    if data.code in used_social_codes:
        print(f"🟠 [BACKEND] Code OAuth ya usado, bloqueando: {data.code[:10]}...")
        raise HTTPException(
            status_code=400,
            detail="Authorization code already used"
        )

    # Marcamos el code como usado ANTES de tocar Google
    used_social_codes.add(data.code)
    print(f"🔵 [BACKEND] Code OAuth registrado como usado: {data.code[:10]}...")

    try:
        user_info = None
        
        if data.provider == "google":
            user_info = await get_google_user(data.code, data.redirect_uri)
        elif data.provider == "github":
            user_info = await get_github_user(data.code, data.redirect_uri)
        elif data.provider == "microsoft":
            user_info = await get_microsoft_user(data.code, data.redirect_uri)
        else:
            raise HTTPException(status_code=400, detail="Proveedor no soportado")

        if not user_info.get("email"):
            raise HTTPException(status_code=400, detail="No se pudo obtener el email del proveedor")

        # 1. Buscar usuario en BD (buscamos la combinación de email y proveedor)
        from ..crud import get_user_by_email_and_provider
        user = await get_user_by_email_and_provider(user_info["email"], data.provider)
        
        if user:
            print(f"🟢 [BACKEND] Usuario existente encontrado: {user['email']}")
        else:
            print(f"🟡 [BACKEND] Usuario no existe. Creando nuevo usuario con email: {user_info['email']}")
            user = await create_oauth_user({
                "email": user_info["email"],
                "username": user_info["username"],
                "provider": data.provider,
                "provider_id": user_info["provider_id"]
            })
            print(f"🟢 [BACKEND] Nuevo usuario creado exitosamente: {user['_id']}")

        # 2. Generar Token
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user["email"], "provider": user["provider"]},
            expires_delta=access_token_expires
        )

        print(f"🟢 [BACKEND] Token generado exitosamente para: {user['email']}")

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": str(user["_id"]) if "_id" in user else user["id"],
                "email": user["email"],
                "username": user["username"],
                "provider": user.get("provider", "local"),
                "created_at": user.get("created_at")
            }
        }

    except SocialAuthError as e:
        print(f"Error social auth: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        print(f"Error interno social login: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Error interno en login social")
