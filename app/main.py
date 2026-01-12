# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from datetime import datetime
import os

from .database import Database, initialize_database
from .routes import auth, users, projects

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manejar ciclo de vida de la aplicación"""
    # Al iniciar
    logger.info("🚀 Iniciando aplicación FastAPI...")
    
    try:
        # Usar la función mejorada de inicialización
        success = await initialize_database()
        if success:
            logger.info("✅ Base de datos inicializada correctamente")
        else:
            logger.warning("⚠️ Base de datos no disponible, algunas funciones no funcionarán")
    except Exception as e:
        logger.error(f"❌ Error durante la inicialización: {e}")
        # No levantamos la excepción para que la app pueda iniciar
    
    yield  # ← La aplicación corre aquí
    
    # Al cerrar
    logger.info("🛑 Cerrando aplicación...")
    
    try:
        await Database.close_mongo_connection()
        logger.info("✅ Conexiones cerradas correctamente")
    except Exception as e:
        logger.error(f"❌ Error cerrando conexiones: {e}")

# Crear aplicación FastAPI
app = FastAPI(
    title="Filament Path Generator API",
    description="API para gestión de proyectos de impresión 3D",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",  # Esto está bien
    redoc_url="/redoc"  # Esto debería estar presente
)

# Configurar CORS para Vercel
# 🔴 IMPORTANTE: Quita la barra final de la URL
origins = [
    "https://pw-app-filament-winding.vercel.app",  # Sin barra final
    "http://localhost:3000",
    "http://localhost:8000",  # Para Swagger local
]

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