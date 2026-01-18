# app/auth.py - MODIFICADO PARA USAR FUNCIONES ASYNC
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#print("🔑 SECRET_KEY cargada:", SECRET_KEY)
#print("🔐 ALGORITHM:", ALGORITHM)

# ==================== FUNCIONES DE CONTRASEÑA ====================

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# ==================== FUNCIONES DE JWT ====================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crear token JWT"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

# ==================== FUNCIONES DE BLACKLIST CON MONGODB ====================

async def blacklist_token(token: str, user_email: str = None):
    """Agregar token a la lista negra en MongoDB"""
    print(f"🔍 DEBUG blacklist_token: {token[:30]}... para {user_email}")
    
    try:
        from .database import get_blacklisted_tokens_collection
        
        print("🔍 DEBUG: Obteniendo colección...")
        blacklist_collection = await get_blacklisted_tokens_collection()
        
        # Verificar si ya existe
        print("🔍 DEBUG: Verificando si ya existe...")
        existing = await blacklist_collection.find_one({"token": token})
        if existing:
            print(f"🔍 DEBUG: Token ya existe en blacklist: {existing}")
            return True
        
        try:
            # Decodificar el token para obtener expiración
            print("🔍 DEBUG: Decodificando token para obtener expiración...")
            payload = jwt.decode(
                token, 
                SECRET_KEY, 
                algorithms=[ALGORITHM],
                options={"verify_exp": False}
            )
            
            exp_timestamp = payload.get("exp")
            expires_at = datetime.fromtimestamp(exp_timestamp) if exp_timestamp else None
            print(f"🔍 DEBUG: Token expira en: {expires_at}")
            
            # Crear documento
            blacklisted_token = {
                "token": token,
                "user_email": user_email,
                "blacklisted_at": datetime.utcnow(),
                "expires_at": expires_at,
                "reason": "user_logout"
            }
            
            print(f"🔍 DEBUG: Insertando: {blacklisted_token}")
            # Insertar en MongoDB
            result = await blacklist_collection.insert_one(blacklisted_token)
            print(f"🔍 DEBUG: Insertado con ID: {result.inserted_id}")
            return True
            
        except jwt.JWTError as e:
            print(f"🔍 DEBUG: Error decodificando token: {e}")
            # Si el token no se puede decodificar, usar expiración por defecto
            blacklisted_token = {
                "token": token,
                "user_email": user_email,
                "blacklisted_at": datetime.utcnow(),
                "expires_at": datetime.utcnow() + timedelta(hours=1),
                "reason": "invalid_token_format"
            }
            
            print(f"🔍 DEBUG: Insertando con expiración por defecto")
            await blacklist_collection.insert_one(blacklisted_token)
            return True
            
    except Exception as e:
        print(f"🔍 DEBUG: Error en blacklist_token: {e}")
        import traceback
        traceback.print_exc()
        return False

async def is_token_blacklisted(token: str) -> bool:
    """Verificar si el token está en la lista negra de MongoDB"""
    print(f"🔍 DEBUG is_token_blacklisted: {token[:30]}...")
    
    try:
        from .database import get_blacklisted_tokens_collection
        
        print("🔍 DEBUG: Obteniendo colección...")
        blacklist_collection = await get_blacklisted_tokens_collection()
        
        # Buscar token activo (no expirado)
        print("🔍 DEBUG: Buscando en MongoDB...")
        blacklisted = await blacklist_collection.find_one({
            "token": token,
            "$or": [
                {"expires_at": {"$gt": datetime.utcnow()}},  # No ha expirado
                {"expires_at": {"$exists": False}}  # No tiene expiración
            ]
        })
        
        if blacklisted:
            print(f"🔍 DEBUG: Token ENCONTRADO en blacklist: {blacklisted}")
        else:
            print("🔍 DEBUG: Token NO encontrado en blacklist")
        
        return blacklisted is not None
        
    except Exception as e:
        print(f"🔍 DEBUG: Error en is_token_blacklisted: {e}")
        import traceback
        traceback.print_exc()
        return False

async def blacklist_all_user_tokens(user_email: str):
    """Agregar todos los tokens activos de un usuario a la blacklist"""
    try:
        from .database import get_blacklisted_tokens_collection
        
        # Por ahora, solo registramos la acción
        # En una implementación completa, buscarías tokens activos del usuario
        
        print(f"⚠️ Blacklist all tokens para {user_email}")
        return True
        
    except Exception as e:
        print(f"❌ Error blacklisting todos los tokens: {e}")
        return False

# ==================== FUNCION DE VERIFICACIÓN DE TOKEN ====================

async def verify_token(token: str):
    """Verificar y decodificar token JWT"""
    print(f"🔍 DEBUG verify_token llamado con token: {token[:30]}...")
    
    try:
        # Verificar si el token está en lista negra
        print("🔍 DEBUG: Verificando blacklist...")
        is_black = await is_token_blacklisted(token)
        print(f"🔍 DEBUG: is_token_blacklisted = {is_black}")
        
        if is_black:
            print("🔴 DEBUG: Token encontrado en blacklist, rechazando...")
            return None
            
        print("🔍 DEBUG: Decodificando token...")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        provider: str = payload.get("provider", "local")
        
        if email is None:
            print("🔍 DEBUG: Token no tiene email")
            return None
        
        print(f"🔍 DEBUG: Token válido para email: {email} ({provider})")
        return {"email": email, "provider": provider}
        
    except jwt.ExpiredSignatureError:
        print("🔍 DEBUG: Token expirado")
        return None
    except jwt.JWTError as e:
        print(f"🔍 DEBUG: Error JWT: {e}")
        return None