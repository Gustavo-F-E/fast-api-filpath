# app/database.py
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    client: AsyncIOMotorClient = None
    database = None
    
    @classmethod
    async def connect_to_mongo(cls):
        """Conectar a MongoDB Atlas"""
        mongodb_uri = os.getenv("MONGODB_URI")
        database_name = os.getenv("DATABASE_NAME", "fil-wind")
        
        try:
            cls.client = AsyncIOMotorClient(mongodb_uri)
            cls.database = cls.client[database_name]
            
            # Verificar conexión
            await cls.client.admin.command('ping')
            print("✅ Conectado a MongoDB Atlas")
            
            # Crear índices si no existen
            await cls.create_indexes()
            
        except ConnectionFailure as e:
            print(f"❌ Error de conexión a MongoDB: {e}")
            raise
    
    @classmethod
    async def close_mongo_connection(cls):
        """Cerrar conexión a MongoDB"""
        if cls.client:
            cls.client.close()
            print("🔒 Conexión a MongoDB cerrada")
    
    @classmethod
    async def create_indexes(cls):
        """Crear índices necesarios"""
        # Índices para usuarios
        await cls.database.usuarios.create_index("email", unique=True)
        await cls.database.usuarios.create_index("username", unique=True)
        await cls.database.usuarios.create_index("provider_id", sparse=True)
        
        # Índices para proyectos
        await cls.database.proyectos.create_index("user_id")
        await cls.database.proyectos.create_index([("user_id", 1), ("created_at", -1)])
        await cls.database.proyectos.create_index([("user_id", 1), ("name", 1)])
        
        print("✅ Índices creados/verificados")

# Funciones de ayuda para obtener colecciones
def get_users_collection():
    return Database.database.usuarios

def get_projects_collection():
    return Database.database.proyectos