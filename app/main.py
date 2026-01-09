# app/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from fastapi.staticfiles import StaticFiles



from .database import Database
from .routes import auth, users, projects

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manejar ciclo de vida de la aplicación"""
    # Al iniciar
    logger.info("🚀 Iniciando aplicación FastAPI...")
    await Database.connect_to_mongo()
    yield
    # Al cerrar
    logger.info("🛑 Cerrando aplicación...")
    await Database.close_mongo_connection()

# Crear aplicación FastAPI
app = FastAPI(
    title="Filament Path Generator API",
    description="API para gestión de proyectos de impresión 3D",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS para Vercel
origins = [
    "https://pw-app-filament-winding.vercel.app/",  # Tu frontend
    "http://localhost:3000",           # Desarrollo local
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # URLs de tu Next.js
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(projects.router)

# Ruta de salud
@app.get("/")
async def root():
    return {
        "message": "Bienvenido a Filament Path Generator API",
        "version": "1.0.0",
        "status": "running",
        "database": "connected" if Database.client else "disconnected"
    }

@app.get("/health")
async def health_check():
    """Verificar salud de la API y conexión a MongoDB"""
    try:
        if Database.client:
            await Database.client.admin.command('ping')
            return {
                "status": "healthy",
                "database": "connected",
                "timestamp": "2024-01-01T00:00:00Z"  # Usar datetime real en producción
            }
        else:
            return {
                "status": "unhealthy",
                "database": "disconnected",
                "error": "No hay conexión a MongoDB"
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "error",
            "error": str(e)
        }

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")
