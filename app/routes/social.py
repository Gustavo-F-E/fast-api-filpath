# app/routes/social.py
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from datetime import timedelta

from ..social_auth import get_google_user, get_facebook_user, get_microsoft_user, SocialAuthError
from ..crud import get_user_by_email, create_oauth_user, update_user
from ..auth import create_access_token
from ..schemas import Token

router = APIRouter()

class SocialLoginRequest(BaseModel):
    provider: str
    code: str
    redirect_uri: str

@router.post("/auth/social/login", response_model=Token)
async def social_login(data: SocialLoginRequest):
    """
    Login estándar para redes sociales via Authorization Code Flow.
    Recibe el 'code' del frontend, lo valida en el backend y devuelve JWT.
    """
    try:
        user_info = None
        
        if data.provider == "google":
            user_info = await get_google_user(data.code, data.redirect_uri)
        elif data.provider == "facebook":
            user_info = await get_facebook_user(data.code, data.redirect_uri)
        elif data.provider == "microsoft":
            user_info = await get_microsoft_user(data.code, data.redirect_uri)
        else:
            raise HTTPException(status_code=400, detail="Proveedor no soportado")
            
        # user_info tiene: email, username, provider, provider_id, picture
        if not user_info.get("email"):
             raise HTTPException(status_code=400, detail="No se pudo obtener el email del proveedor")

        # 1. Buscar usuario en BD
        user = await get_user_by_email(user_info["email"])
        
        if user:
            # Usuario existe: verificar si es compatible o linkear
            # En este MVP, si el email coincide, lo logueamos.
            # Opcional: Podríamos actualizar el provider_id si falta
            pass 
        else:
            # Usuario no existe -> Crear
            try:
                user = await create_oauth_user({
                    "email": user_info["email"],
                    "username": user_info["username"],
                    "provider": data.provider,
                    "provider_id": user_info["provider_id"]
                    # picture podría guardarse en un futuro cambio de modelo
                })
            except ValueError as e:
                # Caso raro: race condition o problema de validación
                raise HTTPException(status_code=400, detail=str(e))
        
        # 2. Generar Token
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user["email"]},
            expires_delta=access_token_expires
        )
        
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
