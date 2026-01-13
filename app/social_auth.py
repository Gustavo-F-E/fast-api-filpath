# app/social_auth.py
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

class SocialAuthError(Exception):
    pass

async def get_google_user(code: str, redirect_uri: str):
    """
    Intercambia el code por un token y obtiene la info del usuario de Google.
    """
    token_url = "https://oauth2.googleapis.com/token"
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        raise SocialAuthError("Falta configuración de Google (CLIENT_ID o CLIENT_SECRET)")

    data = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }
    
    async with httpx.AsyncClient() as client:
        # 1. Obtener Token
        response = await client.post(token_url, data=data)
        if response.status_code != 200:
            raise SocialAuthError(f"Error obteniendo token de Google: {response.text}")
            
        token_data = response.json()
        access_token = token_data.get("access_token")
        
        # 2. Obtener Info Usuario
        user_info_response = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        if user_info_response.status_code != 200:
           raise SocialAuthError(f"Error obteniendo perfil de Google: {user_info_response.text}")
           
        user_info = user_info_response.json()
        
        return {
            "email": user_info.get("email"),
            "username": user_info.get("name") or user_info.get("given_name"),
            "provider": "google",
            "provider_id": user_info.get("id"),
            "picture": user_info.get("picture")
        }

async def get_facebook_user(code: str, redirect_uri: str):
    """
    Intercambia el code por un token y obtiene la info del usuario de Facebook.
    """
    token_url = "https://graph.facebook.com/v19.0/oauth/access_token"
    client_id = os.getenv("FACEBOOK_CLIENT_ID")
    client_secret = os.getenv("FACEBOOK_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise SocialAuthError("Falta configuración de Facebook")

    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "code": code,
    }

    async with httpx.AsyncClient() as client:
        # 1. Obtener Token
        response = await client.get(token_url, params=params)
        if response.status_code != 200:
            raise SocialAuthError(f"Error obteniendo token de Facebook: {response.text}")

        token_data = response.json()
        access_token = token_data.get("access_token")

        # 2. Obtener Info Usuario
        user_info_response = await client.get(
            "https://graph.facebook.com/me",
            params={
                "fields": "id,name,email,picture",
                "access_token": access_token
            }
        )
        
        if user_info_response.status_code != 200:
            raise SocialAuthError(f"Error obteniendo perfil de Facebook: {user_info_response.text}")

        user_info = user_info_response.json()
        
        # Facebook no siempre devuelve email
        email = user_info.get("email")
        if not email:
            # Fallback o error, dependiendo de tu lógica. 
            # Para este caso, usaremos el ID como "falso email" o lanzamos error.
             raise SocialAuthError("Facebook no proporcionó el email del usuario.")

        return {
            "email": email,
            "username": user_info.get("name"),
            "provider": "facebook",
            "provider_id": user_info.get("id"),
            "picture": user_info.get("picture", {}).get("data", {}).get("url")
        }

async def get_microsoft_user(code: str, redirect_uri: str):
    """
    Intercambia el code por un token y obtiene la info del usuario de Microsoft.
    """
    token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    client_id = os.getenv("MICROSOFT_CLIENT_ID")
    client_secret = os.getenv("MICROSOFT_CLIENT_SECRET")

    if not client_id or not client_secret:
         raise SocialAuthError("Falta configuración de Microsoft")

    data = {
        "client_id": client_id,
        "scope": "User.Read email openid profile",
        "code": code,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
        "client_secret": client_secret,
    }

    async with httpx.AsyncClient() as client:
        # 1. Obtener Token
        response = await client.post(token_url, data=data)
        if response.status_code != 200:
             raise SocialAuthError(f"Error obteniendo token de Microsoft: {response.text}")

        token_data = response.json()
        access_token = token_data.get("access_token")

        # 2. Obtener Info Usuario
        user_info_response = await client.get(
            "https://graph.microsoft.com/v1.0/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        if user_info_response.status_code != 200:
             raise SocialAuthError(f"Error obteniendo perfil de Microsoft: {user_info_response.text}")

        user_info = user_info_response.json()

        return {
            "email": user_info.get("mail") or user_info.get("userPrincipalName"),
            "username": user_info.get("displayName"),
            "provider": "microsoft",
            "provider_id": user_info.get("id"),
            "picture": None # Microsoft Graph requiere otra llamada para la foto
        }
