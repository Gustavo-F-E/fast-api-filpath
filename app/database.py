# app/database.py
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv
import logging

load_dotenv()

import logging
import dns.resolver

load_dotenv()

# Configurar DNS resolver explícitamente para evitar timeouts con algunos proveedores de internet/VPN
try:
    dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
    dns.resolver.default_resolver.nameservers = ['8.8.8.8', '8.8.4.4']
except Exception as e:
    print(f"No se pudo configurar DNS personalizado: {e}")

logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    database = None
    
    @classmethod
    async def connect_to_mongo(cls):
        """Conectar a MongoDB Atlas"""
        mongodb_uri = os.getenv("MONGODB_URI")
        database_name = os.getenv("DATABASE_NAME", "fil-wind")
        
        if not mongodb_uri:
            logger.error("❌ MONGODB_URI no configurada en variables de entorno")
            return False
        
        try:
            cls.client = AsyncIOMotorClient(mongodb_uri)
            cls.database = cls.client[database_name]
            
            # Verificar conexión
            await cls.client.admin.command('ping')
            logger.info("✅ Conectado a MongoDB Atlas")
            
            # Crear índices si no existen
            await cls.create_indexes()
            
            return True
            
        except ConnectionFailure as e:
            logger.error(f"❌ Error de conexión a MongoDB: {e}")
            cls.client = None
            cls.database = None
            return False
        except Exception as e:
            logger.error(f"❌ Error inesperado conectando a MongoDB: {e}")
            cls.client = None
            cls.database = None
            return False
    
    @classmethod
    async def close_mongo_connection(cls):
        """Cerrar conexión a MongoDB"""
        if cls.client is not None:
            cls.client.close()
            logger.info("🔒 Conexión a MongoDB cerrada")
            cls.client = None
            cls.database = None
    
    @classmethod
    async def create_indexes(cls):
        """Crear índices necesarios"""
        try:
            if cls.database is None:
                logger.warning("⚠️ No hay conexión a DB para crear índices")
                return
            
            # Índices para usuarios
            await cls.database.usuarios.create_index("email", unique=True)
            await cls.database.usuarios.create_index("username", unique=True)
            await cls.database.usuarios.create_index("provider_id", sparse=True)
            
            # Índices para proyectos
            await cls.database.proyectos.create_index("user_id")
            await cls.database.proyectos.create_index([("user_id", 1), ("created_at", -1)])
            await cls.database.proyectos.create_index([("user_id", 1), ("name", 1)])
            
            # 🔴 NUEVO: Índices para blacklisted_tokens
            # Índice TTL para expiración automática
            await cls.database.blacklisted_tokens.create_index(
                "expires_at",
                expireAfterSeconds=0
            )
            
            # Índice para búsquedas rápidas por token
            await cls.database.blacklisted_tokens.create_index(
                "token",
                unique=True
            )
            
            # Índice para búsquedas por usuario
            await cls.database.blacklisted_tokens.create_index("user_email")
            
            # Índice para búsquedas por fecha
            await cls.database.blacklisted_tokens.create_index("blacklisted_at")
            
            logger.info("✅ Índices creados/verificados (incluyendo blacklisted_tokens)")
            
        except Exception as e:
            logger.error(f"❌ Error creando índices: {e}")

# ============================================================
# FUNCIONES DE AYUDA PARA OBTENER COLECCIONES
# ============================================================

async def get_db():
    """Obtener instancia de la base de datos (async)"""
    if Database.database is None:
        await Database.connect_to_mongo()
    return Database.database

async def get_users_collection():
    """Obtener colección de usuarios (async)"""
    db = await get_db()
    return db.usuarios  # Manteniendo tu nombre de colección

async def get_projects_collection():
    """Obtener colección de proyectos (async)"""
    db = await get_db()
    return db.proyectos  # Manteniendo tu nombre de colección

async def get_blacklisted_tokens_collection():
    """Obtener colección de tokens blacklisted (async)"""
    db = await get_db()
    return db.blacklisted_tokens

# ============================================================
# FUNCIONES SÍNCRONAS PARA COMPATIBILIDAD (opcional)
# ============================================================

def get_users_collection_sync():
    """Obtener colección de usuarios (síncrono - para compatibilidad)"""
    if Database.database is None:
        raise RuntimeError("Database not connected. Call connect_to_mongo() first.")
    return Database.database.usuarios

def get_projects_collection_sync():
    """Obtener colección de proyectos (síncrono - para compatibilidad)"""
    if Database.database is None:
        raise RuntimeError("Database not connected. Call connect_to_mongo() first.")
    return Database.database.proyectos

# ============================================================
# INICIALIZACIÓN AUTOMÁTICA (opcional)
# ============================================================

async def initialize_database():
    """Inicializar la base de datos al inicio de la app"""
    success = await Database.connect_to_mongo()
    
    if not success:
        logger.error("❌ Falló la inicialización de la base de datos")
        return False
    
    # Verificar que las colecciones existen
    try:
        db = await get_db()
        collections = await db.list_collection_names()
        logger.info(f"📁 Colecciones disponibles: {collections}")
        
        # Crear colección blacklisted_tokens si no existe
        if "blacklisted_tokens" not in collections:
            await db.create_collection("blacklisted_tokens")
            logger.info("✅ Colección blacklisted_tokens creada")
        
    except Exception as e:
        logger.error(f"❌ Error verificando colecciones: {e}")
    
    return True