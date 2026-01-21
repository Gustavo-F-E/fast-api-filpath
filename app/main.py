# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from datetime import datetime
import os

from .database import Database, initialize_database
from .routes import auth, users, projects, social, liners, machines

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializar recursos al iniciar la aplicación
    await initialize_database()
    try:
        yield
    finally:
        # Cerrar conexiones al apagar
        try:
            await Database.close_mongo_connection()
        except Exception:
            pass

# Crear instancia de FastAPI con manejador de lifespan
app = FastAPI(title="Filament Path Generator API", version="1.0.0", lifespan=lifespan)

# Configuración CORS robusta
raw_origins = [
    "http://localhost:3000", 
    "http://127.0.0.1:3000",
    os.getenv("URL_FRONTEND")
]

# Limpiar las URLs (quitar barra final si existe) y filtrar None
origins = [origin.rstrip('/') for origin in raw_origins if origin]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(social.router)
app.include_router(liners.router)
app.include_router(machines.router)

# ==================== RUTAS BÁSICAS ====================

@app.get("/")
async def root():
    """Ruta raíz de la API"""
    return {
        "message": "Bienvenido a Filament Path Generator API",
        "version": "1.0.0",
        "status": "running",
        "database": "connected" if Database.client else "disconnected",
        "docs": "/docs",
        "health": "/health"
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
                "timestamp": datetime.utcnow().isoformat(),
                "service": "fastapi"
            }
        else:
            return {
                "status": "degraded",
                "database": "disconnected",
                "timestamp": datetime.utcnow().isoformat(),
                "warning": "Base de datos no disponible"
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "error",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }

@app.get("/status")
async def status_check():
    """Información detallada del estado del sistema"""
    return {
        "app": "running",
        "timestamp": datetime.utcnow().isoformat(),
        "database_connected": Database.client is not None,
        "environment": os.getenv("VERCEL_ENV", "development"),
        "region": os.getenv("VERCEL_REGION", "unknown")
    }

# ==================== DOCUMENTACIÓN ====================

@app.get("/docs", include_in_schema=False)
async def get_documentation():
    """Redirigir a Swagger UI"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/docs")

# Nota: Si tienes archivos estáticos, déjalos comentados por ahora
# app.mount("/static", StaticFiles(directory="static"), name="static")