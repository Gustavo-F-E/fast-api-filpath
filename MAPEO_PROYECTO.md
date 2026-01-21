# 📋 Mapeo General del Proyecto - Filament Winding Path Generator

## 🎯 Descripción General

Este es un proyecto **FastAPI** para la generación y gestión de trayectorias de bobinado de filamento para impresoras 3D. La aplicación incluye:

-   **Backend**: API REST con FastAPI y MongoDB
-   **Autenticación**: Sistema de usuarios y proyectos
-   **Visualización**: Generación de gráficos y descargas de archivos
-   **Despliegue**: Configurado para Vercel

**Stack Tecnológico:**

-   FastAPI 0.115.2
-   MongoDB (Motor para async)
-   Pydantic v2
-   Matplotlib para gráficos
-   Python 3.10+

---

## 📁 Estructura del Proyecto

### 📦 Raíz del Proyecto

```
c:\Proyectos\FastAPI\
├── app.py                              # Punto de entrada alternativo (generador de gráficos)
├── run.py                              # Punto de entrada principal (se usa para Vercel)
├── requirements.txt                    # Dependencias del proyecto
├── vercel.json                         # Configuración para despliegue en Vercel
├── .env.example                        # Ejemplo de variables de entorno
├── README.md                           # Documentación (con ejemplos)
├── comandos.txt                        # Notas con comandos útiles
├── generate_plot.py                    # Generador de gráficos
├── download_plot.py                    # Descargador de gráficos
├── generate_and_download_plot.py       # Generador y descargador combinado
```

**Descripción de archivos principales:**

-   **app.py**: API FastAPI simple para generar/descargar gráficos de trayectorias 3D
-   **run.py**: Punto de entrada para el despliegue (importa del módulo app/)
-   **requirements.txt**: 38 dependencias (FastAPI, MongoDB, Matplotlib, etc.)
-   **vercel.json**: Configuración de deployment con Vercel (Python runtime)

---

## 📂 Directorio `/app` (Núcleo de la API)

### Estructura:

```
app/
├── __init__.py
├── main.py                             # Aplicación FastAPI principal
├── database.py                         # Gestión de conexión a MongoDB y creación de índices
├── crud.py                             # Operaciones CRUD generales
├── auth.py                             # Lógica de seguridad y JWT
├── schemas.py                          # Esquemas Pydantic (User, Project, Liner, Machine, Token)
├── social_auth.py                      # (Opcional) Lógica adicional para OAuth
└── routes/                             # Enrutadores de la API
    ├── __init__.py
    ├── auth.py                         # Login/Logout/Registro
    ├── users.py                        # Perfil de usuario
    ├── projects.py                     # Gestión de proyectos
    ├── liners.py                       # Gestión de Liners
    ├── machines.py                     # Gestión de Máquinas
    └── social.py                       # Autenticación Social (Google, GitHub, etc.)
```

### 📋 Descripciones de módulos:

#### **main.py** - Aplicación FastAPI

-   **Configuración de CORS**: Permite solicitudes desde localhost:3000, localhost:5500 y Vercel
-   **Lifespan handler**: Gestiona inicialización y cierre de la aplicación
-   **Inicialización de BD**: Conecta a MongoDB Atlas al iniciar
-   **Documentación**: Swagger UI en `/docs`
-   **Rutas registradas**: Auth, usuarios y proyectos

#### **database.py** - Conexión MongoDB

-   **Motor AsyncIO**: Cliente asincrónico para MongoDB
-   **Método `connect_to_mongo()`**: Conexión a MongoDB Atlas
-   **Manejo de errores**: Logs detallados de conexión
-   **Índices automáticos**: Creación de índices en colecciones
-   **Variables de entorno**: MONGODB_URI y DATABASE_NAME

#### **schemas.py** - Validación de datos

```python
- PyObjectId         # Conversión de IDs de MongoDB para Pydantic v2
- UserBase, UserCreate, UserLogin, UserResponse
- ProjectBase, ProjectCreate, ProjectUpdate, ProjectResponse
- LinerBase, LinerSection, LinerCreate, LinerResponse
- MachineBase, MachineAxis, MachineCreate, MachineResponse
- Token, TokenData, OAuthLogin
```

#### **auth.py** - Autenticación

-   Manejo de contraseñas con bcrypt
-   Generación de tokens JWT
-   Soporte multi-proveedor (email, OAuth)

#### **crud.py** - Operaciones de BD

-   Crear/Leer/Actualizar/Eliminar usuarios y proyectos
-   Manejo de errores y validaciones

#### **routes/**

-   **auth.py**: Endpoints de login, registro, logout
-   **users.py**: Endpoints para gestión de perfiles
-   **projects.py**: Endpoints para CRUD de proyectos

---

## 📂 Directorio `/static`

```
static/
└── (Archivos estáticos servidos por la API)
```

---

## 📂 Directorio `/uso_en_local` (Desarrollo Local - NO producción)

Este directorio contiene scripts de **prueba y desarrollo local**. No se usa en producción.

```
uso_en_local/
├── main.py, main2.py, main3.py        # Scripts de prueba
├── binance.py                          # Pruebas con API Binance
├── clase_capa.py                       # Clases para capas de bobinado
├── corrida_*.py                        # Simulaciones de bobinado
├── extrucion_*.py                      # Análisis de extrusión
├── grafico_*.py                        # Generadores de gráficos
├── simulador_dividendos.py             # Simulador financiero (no relacionado)
├── SIMULADOR_INTERES_COMPUESTO.PY      # Simulador financiero (no relacionado)
├── sabato.ipynb, prueba.ipynb          # Notebooks de Jupyter
├── imagenes/                           # Gráficos generados
│   └── patrones/                       # Patrones de bobinado (JSON y CSV)
└── ... (más archivos de experimentación)
```

**Nota**: Este directorio es para experimentación local, no se incluye en producción.

---



## 📂 Directorios `/imagenes` e `/imagenes_notebook`

```
imagenes/                               # Gráficos y recursos generados
imagenes_notebook/                      # Gráficos de Notebooks
```

---

## 🔧 Flujo de la Aplicación

### Punto de entrada en Vercel:

```
vercel.json → run.py → app/main.py
```

### Punto de entrada local:

```
run.py o app.py → uvicorn
```

### Inicialización:

1. **Lifespan**: Ejecuta `initialize_database()`
2. **Conexión MongoDB**: Conecta a Atlas con MONGODB_URI
3. **Creación de índices**: Establece índices en `usuarios`, `proyectos`, `liners`, `maquinas` y `blacklisted_tokens` (TTL).
4. **Registro de rutas**: Auth, Users, Projects, Liners, Machines, Social.
5. **Listo**: API lista.

---

## 🔌 Endpoints Principales

### De app.py (generador de gráficos):

-   `GET /` → "Hola Mundo"
-   `POST /generate-plot/` → Genera gráfico 3D
-   `GET /download-plot/` → Descarga gráfico
-   `POST /generate-and-download-plot/` → Genera y descarga

### De app/main.py (API principal):

-   `/docs` → Swagger UI
-   `/auth/*` → Autenticación (Login, Registro, Session)
-   `/users/*` → Gestión de usuarios
-   `/projects/*` → Gestión de proyectos
-   `/liners/*` → Gestión de liners
-   `/machines/*` → Gestión de máquinas
-   `/social/*` → Login con proveedores sociales

---

## 🗂️ Archivos de Configuración

| Archivo                | Propósito                                |
| ---------------------- | ---------------------------------------- |
| `requirements.txt`     | Dependencias pip (38 paquetes)           |
| `vercel.json`          | Configuración de despliegue Vercel       |
| `.env` (no versionado) | Variables de entorno (MONGODB_URI, etc.) |
| `comandos.txt`         | Comandos útiles para desarrollo          |

---

## 📊 Dependencias Principales

| Paquete       | Versión | Propósito              |
| ------------- | ------- | ---------------------- |
| fastapi       | 0.115.2 | Framework web          |
| uvicorn       | 0.32.0  | Servidor ASGI          |
| motor         | 3.7.1   | Cliente MongoDB async  |
| pymongo       | 4.16.0  | Driver MongoDB         |
| pydantic      | 2.9.2   | Validación de datos    |
| bcrypt        | 4.0.1   | Hash de contraseñas    |
| python-jose   | 3.5.0   | Tokens JWT             |
| matplotlib    | 3.9.2   | Generación de gráficos |
| python-dotenv | 1.2.1   | Variables de entorno   |
| cryptography  | 46.0.3  | Encriptación           |

---

## 🚀 Cómo Ejecutar

### Local:

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar con uvicorn
uvicorn app.main:app --reload

# O usar:
python run.py
```

### Variables de entorno necesarias:

```
MONGODB_URI=mongodb+srv://usuario:contraseña@cluster.mongodb.net/
DATABASE_NAME=fil-wind
JWT_SECRET_KEY=tu-clave-secreta
```

### Despliegue en Vercel:

```bash
vercel deploy
```

---

## 📈 Resumen Estadístico

| Métrica                      | Cantidad                                  |
| ---------------------------- | ----------------------------------------- |
| **Archivos Python**          | ~30+                                      |
| **Módulos principales**      | 6 (database, auth, crud, schemas, routes) |
| **Rutas implementadas**      | 3 grupos (auth, users, projects)          |
| **Dependencias**             | 38 paquetes                               |
| **Notebooks Jupyter**        | 5 (ejemplos, pruebas)                     |
| **Directorio de desarrollo** | uso_en_local/ (~50 archivos)              |

---

## 🎓 Notas

-   El proyecto usa **async/await** en toda la aplicación
-   MongoDB es la base de datos principal
-   CORS está configurado para desarrollo y producción (Vercel)
-   Los logs se escriben con el nivel INFO
-   El proyecto sigue la estructura modular de FastAPI (routes, schemas, crud)
-   Hay mucho código experimental en `uso_en_local/` que no se usa en producción

---
